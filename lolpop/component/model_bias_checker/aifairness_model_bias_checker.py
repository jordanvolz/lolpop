from lolpop.component.model_bias_checker.base_model_bias_checker import BaseModelBiasChecker
from lolpop.utils import common_utils as utils
from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from omegaconf.listconfig import ListConfig
@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class AIFairnessModelBiasChecker(BaseModelBiasChecker): 

    __REQUIRED_CONF__ = {"config": ["model_target",
                                   "privileged_groups", "unprivileged_groups", 
                                   "favorable_classes", "privileged_classes", 
                                   "protected_attribute_names"]}

    def check_model_bias(self, data, model, *args, **kwargs): 
        """Uses the provided data and model to check for bias in the model's predictions.
            Args:
                data (dict): A dictionary containing the training/testing data.
                model (object): The model trainer object being checked for bias.
        """
        metrics_out = {}
        if self.problem_type == "classification": 
            #set up data/predictions
            df_train = data["X_train"]
            df_train_w_labels = df_train.copy() 
            df_train_w_labels[self._get_config("model_target")] = data["y_train"].values

            #set up aif dataset + configs
            model_target = self._get_config("model_target")
            privileged_groups = self._get_config("privileged_groups")
            unprivileged_groups = self._get_config("unprivileged_groups")
            favorable_classes = self._eval_classes(self._get_config("favorable_classes"))
            privileged_classes = self._eval_classes(self._get_config("privileged_classes"))
            ds = StandardDataset(
                df=df_train_w_labels.dropna(), #NA make AI360 fail 
                label_name=model_target, 
                protected_attribute_names=self._get_config("protected_attribute_names"), 
                favorable_classes=favorable_classes, 
                privileged_classes=privileged_classes,
                )

            #get fairness metrics from binarylabeldatasetmetric. This essentially checks bias in the dataset itself
            bldm = BinaryLabelDatasetMetric(ds, unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
            metrics_out["bldm_base_rate"] = bldm.base_rate() # ratio of priv/total 
            metrics_out["bldm_disparate_impact"] = bldm.disparate_impact() # ratio of prob fav outcomes of non/priv
            metrics_out["bldm_mean_difference"] =  bldm.mean_difference() # diff in probability of favorable outcoems for non vs priv
            metrics_out["bldm_consistency"] = bldm.consistency()[0] # meastures how similar the labels are for similar instanes
            metrics_out["bldm_smoothed_edf"] = bldm.smoothed_empirical_differential_fairness() #

            ds_preds = ds.copy()
            ds_preds.labels = model.predict(data).get("train")

            #get fairness metric from classificationmetric. This checks fairness in predictions
            cm = ClassificationMetric(ds, ds_preds, unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
            metrics_out["cm_tpr_diff"] = cm.true_positive_rate_difference() 
            metrics_out["cm_selection_rate"] = cm.selection_rate() 
            metrics_out["cm_theil_index"] = cm.theil_index() 
            metrics_out["cm_false_positive_rate_ratio"] = cm.false_positive_rate_ratio() 
            metrics_out["cm_false_omission_rate_ratio"] = cm.false_omission_rate_ratio() 
            metrics_out["cm_false_negative_rate_ratio"] = cm.false_negative_rate_ratio()
            metrics_out["cm_false_discovery_rate_ratio"] = cm.false_discovery_rate_ratio() 
            metrics_out["cm_error_rate_ratio"] = cm.error_rate_ratio()  
            metrics_out["cm_differential_fba"] = cm.differential_fairness_bias_amplification()
        else: 
            self.log("Problem type %s not supported for model bias checker %s" %(self.problem_type, self.name))        

        #TODO: we should have bias thresholds, and if any are exceeded, then we can reweigh the dataset
        #via something like: https://aif360.readthedocs.io/en/stable/modules/generated/aif360.algorithms.preprocessing.Reweighing.html
        #will have to think about how this applies in the workflow though.
        #i.e. we may want to move the dataset bias stuff up in the data_processing step. 

        return metrics_out

    def _eval_classes(self, class_list): 
        """Evalutes `lambda` functions defined in configuration into proper python functions. 
           AIF360 allows dynamically specifying classes via lambda notation, but this isn't 
           parsed correctly when defined in yaml files. This function fixes that. 

        Args:
            class_list (list): List of classes

        Returns:
            list_out: list of classes
        """
        list_out = []
        for cl in class_list:
            if isinstance(cl, str) and  cl.startswith("lambda x"): 
                cl = eval(cl) #we should rework this in the future 
            elif isinstance(cl, list) or isinstance(cl, ListConfig): 
                cl = self._eval_classes(cl)
            list_out.append(cl)  
        return list_out      