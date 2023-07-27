from lolpop.component.model_explainer.base_model_explainer import BaseModelExplainer
from lolpop.utils import common_utils as utils
import alibi.explainers as alibi
import shap 
import os
from matplotlib import pyplot as plt
import numpy as np

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class AlibiModelExplainer(BaseModelExplainer): 
    __REQUIRED_CONF__ = {
        "config" : ["explainer_class", "local_dir"]
    }

    def get_explanations(self, data, model, model_version, label, classification_type=None, to_list=False, skip_explainer_plots=True, *args, **kwargs): 
        """This method generates SHAP-based feature importance scores for a given model and input data. If skip_explainer_plots is True, only the feature importance scores will be returned in Alibi format. If it is False, the method will save the SHAP summary and dependence plots as artifacts.

        Args:
        data (pandas.DataFrame): The input data to explain the model.
        model (object): The machine learning model we wish to explain.
        model_version (string): The model version object obtain from the metadata_tracker.
        label (string): The model targeta.
        classification_type (string): The type of classification. This parameter is only used if the problem type is classification. 
        to_list (boolean): If True the returned explanations will be in a list format.
        skip_explainer_plots (boolean): If True, the skip the SHAP plots.=

        Returns:
        A dictionary containing SHAP explainer and SHAP values.
        """
        #load explainer class and instatiate
        explainer_class = self._get_config("explainer_class")
        explainer_cl = getattr(alibi, explainer_class)
        explainer = explainer_cl(model._get_model(), task=self.problem_type, feature_names=data.columns.to_list())

        #fit the explainer and generate explanations
        explainer.fit()
        explanations = explainer.explain(data)

        #generate shap_plots 
        if not skip_explainer_plots:
            self._get_shap_plots(explanations.shap_values, explanations.expected_value, data, model._get_model(), label, model_version, classification_type)

        #log feature importance         
        self.metadata_tracker.log_metadata(model_version, id = "%s_global_feature_importance" %label, data = explanations.raw.get("importances").get("aggregated"))
  
        if to_list: 
            explanations = explanations.raw.get("instances").tolist() 

        return explanations

    def get_feature_importance(self, data_dict, model, model_version, *args, **kwargs): 
        """ This method generates SHAP-based feature importance scores for train and test sets. It saves SHAP summary and dependence plots as artifacts. 

        Args:
        data_dict (dict): A dictionary of the input data to explain.
        model (object): The machine learning model we wish to explain.
        model_version (string): The model version object obtain from the metadata_tracker.

        Returns:
        Tuple of two Alibi data objects:
        - the SHAP-based feature importance for the training set.
        - the SHAP-based feature importance for the test set.
        """
        #generate train/test datasets
        (train_X, train_y), (test_X, test_y) = self.data_splitter.get_train_test_dfs(data_dict, combine_xy=False) 
        if self.problem_type == "classification": 
            classification_type = utils.get_multiclass(train_y.unique())
        else: 
            classification_type = None 

        skip_explainer_plots = self._get_config("skip_explainer_plots", False)
        explanations_train = self.get_explanations(train_X, model, model_version, "train", classification_type, skip_explainer_plots=skip_explainer_plots)
        explanations_test = self.get_explanations(test_X, model, model_version, "test", classification_type, skip_explainer_plots=True)

        #compare test and train 
        expected_value_diff, feature_importance_diff = self._compare_train_test_feat_importance(explanations_train, explanations_test, classification_type)
        
        #log feature importance
        self.metadata_tracker.log_metadata(model_version, id = "feature_importance_expected_value_diff_train_test", data = expected_value_diff)
        self.metadata_tracker.log_metadata(model_version, id = "feature_importance_feature_value_diff_train_test", data = feature_importance_diff)

        return explanations_train, explanations_test

    #generate all the shap plot
    def _get_shap_plots(self, shap_values, expected_value, data, model, label, model_version, classification_type=None): 
        """This method generates various SHAP plots for the given SHAP values and saves them as artifacts.

        Args:
        shap_values (numpy.ndarray): The SHAP values to generate the plots.
        expected_value (float): The expected value of the model.
        data (pandas.DataFrame): The input data to the model.
        model (object): The machine learning model to explain.
        label (string): A label for the data.
        model_version (string): The model version.
        classification_type (string): The type of classification.

        Returns:
        None.
        """
        #note: classificaiton_type == None currently when making a prediction
        if classification_type == "multiclass":
            #bar plot w/ all classes
            shap.summary_plot(shap_values, data, show=False)
            self._save_pyplot("shap_summary_plot_bar", label, model_version)
        else:
            expected_value = [expected_value] 

        
        for i in range(len(shap_values)):
            ##Note: for multiclass, many plots only work on one class at a time.
            class_str = "" 
            if classification_type == "multiclass": 
                class_str = "_" + str(i)
            #scatter plot for class
            shap.summary_plot(shap_values[i], data, show=False)
            self._save_pyplot("shap_summary_plot_scatter%s" %class_str, label, model_version)

            #bar plot for class
            shap.summary_plot(shap_values[i], data, plot_type="bar", show=False)
            self._save_pyplot("shap_summary_plot_bar%s" %class_str, label, model_version)

            ##force plot for class
            ##force plot is very slow for large matrices, so we'll impose a sample
            sample_size = 100
            idx = np.random.randint(len(shap_values[i]), size=sample_size)
            # force plot doesn't really work w/ multiclass right now
            if classification_type !="multiclass":
                hplt = shap.force_plot(expected_value[i], shap_values[i][idx,:], data.loc[idx] ,show=False)
                force_html = "<head>%s</head> <body>%s</body>" %(shap.getjs(), hplt.html())
                self._save_file("shap_force_plot_bar%s" %class_str, label, force_html, model_version)

            #decision plots
            shap.decision_plot(expected_value[i], shap_values[i][idx,:], show=False)
            self._save_pyplot("shap_decision_plot%s" %class_str, label, model_version)

            #create dependence plots -- one for each feature
            for ft in data.columns: 
                #you can set interaction_index to determine which feature is used to color plot.
                #if omitted it will just use what seems to have the best interaction. If none it will turn off coloring
                shap.dependence_plot(ft, shap_values[i], data, interaction_index=None, show=False)
                self._save_pyplot("shap_dependence_plot%s_%s" %(class_str, ft), label, model_version)\

                #partial dependenceplots
                if i == 0: #only need to calculate these once
                    shap.partial_dependence_plot(ft, model.predict, data, show=False)
                    self._save_pyplot("shap_partial_dependence_plot_%s" %ft, label, model_version)

            # we can also check bias too if not doing it elsewhere: 
            #for bias in config.get('BIAS_COLUMNS').split(","): 
            #    shap.group_difference_plot(shap_values[i], data[bias].values==1, feature_names=data.columns)
            #    save_pyplot("shap_group_difference_plot_%s_bias_%s" %(str(i),bias), label, model_version)
            
            #waterfall_plot only shows the effect of one row at a time
            #need to construct proper exp[lanation object for this plot instead of using alibi wrapper
            shap_ex = shap._explanation.Explanation(shap_values[i], base_values=expected_value)
            shap.waterfall_plot(shap_ex[0], show=False)
            self._save_pyplot("shap_waterfall_example%s" %class_str, label, model_version)

            #heatmap
            #commenting out because this takes a long time to generate
            #shap.plots.heatmap(shap_ex)
            #self._save_pyplot("shap_heatmap%s" %class_str, label, model_version)
            
            #other plots
            #multioutput_decision_plot only shows the effect of one row at a time, but it's super awesome for multiclass problems
            
   #save shapley plut using matplotlib.pyplot
    def _save_pyplot(self, name, label, model_version): 
        """This method saves the generated SHAP plot as an artifact.

        Args:
        name (string): A name for the plot.
        label (string): The label of the data.
        model_version (string): The model version object obtained from the metadata_tracker.

        Returns:
        The saved artifact.
        """
        local_path = "%s/%s/%s" %(self._get_config("local_dir"), self.metadata_tracker.get_resource_id(model_version), label)
        os.makedirs(local_path, exist_ok=True)
        key = "%s_%s"%(name, label)
        local_file = "%s/%s.png" %(local_path, key)
        plt.savefig(local_file)
        artifact = self.metadata_tracker.log_artifact(model_version, id = key, path = local_file, external=False)
        #plt.clf()
        plt.close()

        return artifact

    def _save_file(self, name, label, content, model_version, extension="html"): 
        """This method saves the generated SHAP plot to a file as an artifact.

        Args:
        name (string): A name for the file.
        label (string): The label of the data.
        content (string): The content of the file.
        model_version (string): The version of the model to explain.
        extension (string): The extension of the file.

        Returns:
        The saved artifact.
        """
        local_path = "%s/%s/%s" % (self._get_config("local_dir"),self.metadata_tracker.get_resource_id(model_version), label)
        os.makedirs(local_path, exist_ok=True)
        key = "%s_%s" % (name, label)
        local_file = "%s/%s.%s" % (local_path, key, extension)
        with open(local_file, "w+") as f: 
            f.write(content)
        artifact = self.metadata_tracker.log_artifact(model_version, id=key, path=local_file, external=False)
 
        return artifact

    def _compare_train_test_feat_importance(self, explanations_train, explanations_test, classification_type, threshold=0.25): 
        """This method compares the SHAP-based feature importance scores between the train and test sets. 

        Args:
        explanations_train (pandas.DataFrame): The SHAP-based feature importance for the training set.
        explanations_test (pandas.DataFrame): The SHAP-based feature importance for the test set.
        classification_type (string): The type of classification.
        threshold (float): A threshold value for checking the differences between train and test sets.

        Returns:
        Tuple containing the expected differences and the feature importance differences.
        """

        #shap_train = explanations_train.shap_values
        #shap_test = explanations_test.shap_values

        #make everything 3dim so the following code is the same regardless of type
        #if classification_type !="multiclass": 
        #    shap_train = [shap_train]
        #    shap_test = [shap_test]

        #check expected values 
        if classification_type == "multiclass": 
            expected_diff = [(x - y)/max(x, 0.00001) for x,y in zip(explanations_train.expected_value, explanations_test.expected_value)]
        else: 
            expected_diff = [(explanations_train.expected_value -
                             explanations_test.expected_value)/max(explanations_train.expected_value, 0.00001)]

        for x in expected_diff: 
            if x> threshold: 
                self.notify("Threshold exceeded in difference between train/test shap expected values.")

        #check avg value for feature
        # we could recalculate everything, but shap provides the globals in the aggregated features
        #np_train = np.array(shap_train)
        #train_ft_values = np.abs(np_train).mean(axis=0).mean(axis=0)
        #np_test = np.array(shap_test)
        #test_ft_values = np.abs(np_test).mean(axis=0).mean(axis=0)

        raw_train_importances = explanations_train.raw.get("importances").get("aggregated")
        raw_test_importances = explanations_test.raw.get("importances").get("aggregated")
        # sort values to ensure features match up
        train_ft_values = sorted(
            [ x[1] for x in  zip(raw_train_importances.get("names"), raw_train_importances.get("ranked_effect"))] 
            ) 
        test_ft_values = sorted(
            [ x[1] for x in  zip(raw_test_importances.get("names"), raw_test_importances.get("ranked_effect"))]
            ) 

        feature_diff = [(x-y)/max(x, 0.00001) for x,y in zip(train_ft_values, test_ft_values)]

        for x in feature_diff: 
            if x > threshold: 
                self.notify("Threshold exceeded in difference between a feature shap value impact in train & test datasets.")

        return expected_diff, feature_diff
 
