from lolpop.pipeline.train.base_train import BaseTrain
from lolpop.utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class OfflineTrain(BaseTrain): 
    __REQUIRED_CONF__ = {
        "components": ["data_splitter", "metadata_tracker", "model_checker", "model_explainer", "model_visualizer", "model_bias_checker"], 
        "config": []
    }

    def split_data(self, data, **kwargs): 
        #split data. returns dictionary of train/vali/test dataframes
        data_dict = self.data_splitter.split_data(data)
        
        return data_dict

    def train_model(self, data, *args, **kwargs): 
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

    def check_model(self, data_dict, model, model_version, **kwargs):
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


    def analyze_model(self, data_dict, model, model_version, **kwargs): 
        #calculate feature importance
        self.model_explainer.get_feature_importance(data_dict, model, model_version)
         
        #compare model to baseline
        self.model_checker.get_baseline_comparison(data_dict, model, model_version)

        #create some eye candy
        self.model_visualizer.generate_viz(data_dict, model._get_model(), model_version)


    def compare_models(self, data_dict, model, model_version): 
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

    def check_model_bias(self, data_dict, model, model_version):
        #check model bias
        self.model_bias_checker.check_model_bias(data_dict, model, model_version)

    def retrain_model_on_all_data(self, data, model_version, ref_model = None):
        if hasattr(self, "model_trainer"):  
            model, experiment = self.model_trainer.rebuild_model(data, model_version)
        else: 
            #if no model_trainer is specified in config, we can rebuild using the winning_exp_model_trainer
            winning_exp_model = self.metadata_tracker.load_model(None, model_version, ref_model=ref_model)
            model, experiment = winning_exp_model.rebuild_model(data, model_version)
            return model, experiment
