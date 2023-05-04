from lolpop.component.model_bias_checker.base_model_bias_checker import BaseModelBiasChecker
from lolpop.utils import common_utils as utils
from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class AIFairnessModelBiasChecker(BaseModelBiasChecker): 

    def check_model_bias(self, data, model, model_version, *args, **kwargs): 
        #set up data/predictions
        df_train = data["X_train"]
        df_train_w_labels = df_train.copy() 
        df_train_w_labels[self._get_config("model_target")] = data["y_train"].values
        preds = model.predict(data).get("train")

        #set up aif dataset + configs
        model_target = self._get_config("model_target")
        privileged_groups = self._get_config("privileged_groups")
        unprivileged_groups = self._get_config("unprivileged_groups")
        ds = StandardDataset(
            df=df_train_w_labels.dropna(), #NA make AI360 fail 
            label_name=model_target, 
            protected_attribute_names=self._get_config("protected_attribute_names"), 
            favorable_classes=self._get_config("favorable_classes"), 
            privileged_classes=self._get_config("privileged_classes"),
            )

        #get fairness metrics from binarylabeldatasetmetric. This essentially checks bias in the dataset itself
        bldm = BinaryLabelDatasetMetric(ds, unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
        self.metrics_tracker.log_metric(model_version, "bldm_base_rate", bldm.base_rate()) # ratio of priv/total 
        self.metrics_tracker.log_metric(model_version, "bldm_disparate_impact", bldm.disparate_impact()) # ratio of prob fav outcomes of non/priv
        self.metrics_tracker.log_metric(model_version, "bldm_mean_difference",  bldm.mean_difference()) # diff in probability of favorable outcoems for non vs priv
        self.metrics_tracker.log_metric(model_version, "bldm_consistency", bldm.consistency()[0]) # meastures how similar the labels are for similar instanes
        self.metrics_tracker.log_metric(model_version, "bldm_smoothed_edf", bldm.smoothed_empirical_differential_fairness()) #

        ds_preds = ds.copy()
        ds_preds.labels=preds

        #get fairness metric from classificationmetric. This checks fairness in predictions
        cm = ClassificationMetric(ds, ds_preds, unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
        self.metrics_tracker.log_metric(model_version, "cm_tpr_diff", cm.true_positive_rate_difference()) 
        self.metrics_tracker.log_metric(model_version, "cm_selection_rate", cm.selection_rate()) 
        self.metrics_tracker.log_metric(model_version, "cm_theil_index", cm.theil_index()) 
        self.metrics_tracker.log_metric(model_version, "cm_false_positive_rate_ratio", cm.false_positive_rate_ratio()) 
        self.metrics_tracker.log_metric(model_version, "cm_false_omission_rate_ratio", cm.false_omission_rate_ratio()) 
        self.metrics_tracker.log_metric(model_version, "cm_false_negative_rate_ratio", cm.false_negative_rate_ratio())
        self.metrics_tracker.log_metric(model_version, "cm_false_discovery_rate_ratio", cm.false_discovery_rate_ratio()) 
        self.metrics_tracker.log_metric(model_version, "cm_error_rate_ratio", cm.error_rate_ratio())  
        self.metrics_tracker.log_metric(model_version, "cm_differential_fba", cm.differential_fairness_bias_amplification())
        
        #TODO: we should have bias thresholds, and if any are exceeded, then we can reweigh the dataset
        #via something like: https://aif360.readthedocs.io/en/stable/modules/generated/aif360.algorithms.preprocessing.Reweighing.html
        #will have to think about how this applies in the workflow though.
        #i.e. we may want to move the dataset bias stuff up in the data_processing step. 