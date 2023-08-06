from lolpop.pipeline.train.base_train import BaseTrain
from lolpop.utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class OfflineTrain(BaseTrain): 
    __REQUIRED_CONF__ = {
        "components": ["data_splitter", "metadata_tracker", "resource_version_control", "model_checker", "model_explainer", "model_visualizer", "model_bias_checker"], 
        "config": []
    }

    def split_data(self, data, *args, **kwargs): 
        """
        Split the input data into train/validation/test sets using the data splitter configured 
        in the class. 
        
        Args:
            data (object): A DataFrame containing the input data to be split.

        Returns:
            A dictionary with train/test/validation data where each is a 
            DataFrame containing the corresponding split.
        """

        #split data. returns dictionary of train/vali/test dataframes
        data_dict = self.data_splitter.split_data(data)
        
        return data_dict

    def train_model(self, data, *args, **kwargs): 
        """
        Train a machine learning model using the input data and return the trained model and model version. 
        If a hyperparameter tuner is configured in the class, the tuner will be used to search for the optimal 
        hyperparameters for the model.
        
        Args:
            data (object): A dictionary containing three data splits "train_data", "val_data" and "test_data", as 
                  returned by the split_data method.
            *args: Additional non-keyword arguments.
            **kwargs: Optional keyword arguments to pass to the model trainer.

        Returns:
            A tuple of the trained model and model version.
        """

        #create model_version
        id = self._get_config("model_name")
        model_version = self.metadata_tracker.create_resource(id, type="model_version")
    
        #if we are using hyperparameter tuner, use that, otherwise just use the model trainer provided
        if hasattr(self, "hyperparameter_tuner"): 
            model = self.hyperparameter_tuner.run_experiment(data, model_version)
        else: 
            #TODO: this needs a better entry point. build_model doesn't actually log stuff
            model, _  = self.model_trainer.build_model(data, model_version)

        return model, model_version

    def check_model(self, data_dict, model, model_version, *args, **kwargs):
        """
        Perform model checks on the input data and trained model, log the results in the 
        metadata tracker, and notify via email if any issues are found with the checks. 
        
        Args:
            data_dict (object): A dictionary containing split data, as 
                       returned by the split_data method.
            model (object): The trained machine learning model to be checked.
            model_version (object): The version of the model being checked.
            **kwargs: Optional keyword arguments to pass to the model checker.
        """

        #run model checks
        model_report, file_path, checks_status = self.model_checker.check_model(data_dict, model)

        #log model report to metadata tracker
        self.metadata_tracker.log_checks(
            model_version,
            file_path = file_path, 
            report = model_report, 
            checker_class = type(self.model_checker).__name__, 
            type="model"
            )

        if checks_status == "ERROR" or checks_status == "WARN": 
            url = self.metadata_tracker.url
            self.notify("Issues found with model checks. Visit %s for more information." %url, checks_status)


    def analyze_model(self, data_dict, model, model_version, *args, **kwargs): 
        """
        Generate feature importance plots, compare the model and data to a baseline, 
        and generate visualizations to assist in model analysis. 
        
        Args:
            data_dict (object): A dictionary containing three data splits, as 
                       returned by the split_data method.
            model (object): The trained machine learning model to be analyzed.
            model_version (object): The version of the model to be analyzed.
            **kwargs: Optional keyword arguments to pass to the model explainer, baseline comparison, and 
                      model visualizer.
        """
        #calculate feature importance
        self.model_explainer.get_feature_importance(data_dict, model, model_version)
         
        #compare model to baseline
        self.model_checker.get_baseline_comparison(data_dict, model, model_version)

        #create some eye candy
        self.model_visualizer.generate_viz(data_dict, model._get_model(), model_version)


    def compare_models(self, data_dict, model, model_version, *args, **kwargs): 
        """
        Compare the current model to the previously deployed model, log the comparison results in the 
        metadata tracker, and return a boolean indicating if the current model is an improvement over 
        the previous model. 
        
        Args:
            data_dict (object): A dictionary containing three data splits, as 
                       returned by the split_data method.
            model (object): The trained machine learning model to be analyzed.
            model_version (object): The version of the model being tested for improvement.
            
        Returns:
            A boolean indicating if the current model is an improvement over the previous model. 
            If there is no previous model to compare to, will return True.
        """
        #get currently deployed model version/previous model version and winning experiment
        prev_model_version = self.metadata_tracker.get_currently_deployed_model_version(model_version)

        if prev_model_version is not None: 
            prev_experiment = self.metadata_tracker.get_winning_experiment(prev_model_version)

            #get the prev model version object from resource version control and load it into a model trainer
            prev_model_obj = self.resource_version_control.get_model(prev_experiment)
            prev_model = self.metadata_tracker.load_model(prev_model_obj, model_version, model)

            #compare model to the last version 
            report, file_path = self.model_checker.calculate_model_drift(data_dict, model, prev_model)
            self.metadata_tracker.log_artifact(model_version, id="model_drift_report", path = file_path, external = False)
            is_new_model_better = self.model_checker.compare_models(data_dict, model, prev_model, model_version, prev_model_version)
            
            return is_new_model_better 
        
        else: 
            self.log("No previous model version found for model: %s" %self.metadata_tracker.get_resource_id(model_version))
            return True 

    def check_model_bias(self, data_dict, model, model_version, *args, **kwargs):
        """
        Check for bias in the input data and trained model and log the results in the metadata tracker. 
        
        Args:
            data_dict (object): A dictionary containing three data splits, as 
                       returned by the split_data method.
            model (object): The trained machine learning model to be checked for bias.
            model_version (object): The version of the model to be checked for bias.
        """
        #check model bias
        bias_metrics = self.model_bias_checker.check_model_bias(data_dict, model)
        for k,v in bias_metrics.items(): 
            self.metrics_tracker.log_metric(model_version, k, v)

    def retrain_model_on_all_data(self, data, model_version, ref_model = None):
        """
        Retrain a machine learning model on all available data and return the new trained model and model version. 
        
        Args:
            data (object): A DataFrame containing all the data to be used for retraining.
            model_version (object): The version of the model to be retrained.
            ref_model (object): The previous model to be used as reference.

        Returns:
            A tuple of the trained model and model version.
        """
        if hasattr(self, "model_trainer"):  
            model, experiment = self.model_trainer.rebuild_model(data, model_version)
        else: 
            #if no model_trainer is specified in config, we can rebuild using the winning_exp_model_trainer
            winning_exp_model = self.metadata_tracker.load_model(None, model_version, ref_model=ref_model)
            model, experiment = winning_exp_model.rebuild_model(data, model_version)
            return model, experiment
