from lolpop.pipeline.train.base_train import BaseTrain
from lolpop.utils import common_utils as utils
from lolpop.utils import metaflow_utils as meta_utils
from metaflow import FlowSpec, step
from pathlib import Path

METAFLOW_CLASS = "MetaflowOfflineTrainSpec"
PLUGIN_PATHS = "plugin_paths.txt"


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class MetaflowOfflineTrain(BaseTrain):
    __REQUIRED_CONF__ = {
        "components": ["data_splitter", "metadata_tracker", "model_checker", "model_explainer", "model_visualizer", "model_bias_checker"],
        "config": []
    }

    def run(self, data, **kwargs):
        #get flow class object from this file
        mod_cl = meta_utils.get_flow_class(__file__, METAFLOW_CLASS)

        flow = meta_utils.load_flow(
            mod_cl, self, PLUGIN_PATHS, data=data)
        self.log("Loaded metaflow flow %s" % METAFLOW_CLASS)

        meta_utils.run_flow(flow, "run", __file__, PLUGIN_PATHS)
        self.log("Metaflow pipeline %s finished." % METAFLOW_CLASS)

    def get_artifacts(self, artifact_keys):
        #get latest run of this pipeline
        run = meta_utils.get_latest_run(METAFLOW_CLASS)

        #get requested artifacts
        artifacts = meta_utils.get_run_artifacts(
            run, artifact_keys, METAFLOW_CLASS)

        return artifacts


class MetaflowOfflineTrainSpec(FlowSpec):

    def __init__(self, lolpop=None, data=None, use_cli=False, **kwargs):
        #you need to set local attributes before calling super
        #only the first time we create the class will these parameters be provided.
        #The rest of the calls are metaflow internal calls and we do not want to reset them
        if lolpop is not None:
            self.lolpop = lolpop
        if data is not None:
            self.data = data

        #load plugins
        meta_utils.load_plugins(PLUGIN_PATHS)

        #call init -- this kicks off the main workflow
        super().__init__(use_cli=use_cli)

    @step
    def start(self):
        self.next(self.split_data)

    @step
    def split_data(self):
        #split data. returns dictionary of train/vali/test dataframes
        data_dict = self.lolpop.data_splitter.split_data(self.data)
        self.data_dict = data_dict

        self.next(self.train_model)

    @step
    def train_model(self):
        #create model_version
        id = self.lolpop._get_config("model_name")
        model_version = self.lolpop.metadata_tracker.create_resource(id, type="model_version")
        print(model_version)
        print(model_version[1])
        print(model_version[1].info.run_id)
        print(type(model_version[1]))

        #if we are using hyperparameter tuner, use that, otherwise just use the model trainer provided
        if hasattr(self.lolpop, "hyperparameter_tuner"):
            model = self.lolpop.hyperparameter_tuner.run_experiment(
                self.data_dict, model_version)
        else:
            model = self.lolpop.model_trainer.build_model(self.data_dict, model_version)

        self.model = model 
        self.model_version = model_version 

        self.next(self.analyze_model)

    @step    
    def check_model(self):
        #run model checks
        model_report, file_path, checks_status = self.lolpop.model_checker.check_model(
            self.data_dict, self.model)

        #log model report to metadata tracker
        self.lolpop.metadata_tracker.log_checks(
            self.model_version,
            file_path=file_path,
            report=model_report,
            checker_class=self.lolpop.model_checker.name,
            type="model"
        )

        if checks_status == "ERROR" or checks_status == "WARN":
            url = self.lolpop.metadata_tracker.url
            self.lolpop.notify(
                "Issues found with model checks. Visit %s for more information." %url, checks_status)
            
        self.next(self.check_model_bias)

    @step
    def analyze_model(self):
        #calculate feature importance
        self.lolpop.model_explainer.get_feature_importance(
            self.data_dict, self.model, self.model_version)

        #compare model to baseline
        self.lolpop.model_checker.get_baseline_comparison(
            self.data_dict, self.model, self.model_version)

        #create some eye candy
        self.lolpop.model_visualizer.generate_viz(
            self.data_dict, self.model._get_model(), self.model_version)
        
        self.next(self.check_model)

    @step
    def compare_models(self):
        #get currently deployed model version/previous model version and winning experiment
        prev_model_version = self.lolpop.metadata_tracker.get_currently_deployed_model_version(
            self.model_version)

        if prev_model_version is not None:
            prev_experiment = self.lolpop.metadata_tracker.get_winning_experiment(
                prev_model_version)

            #get the prev model version object from resource version control and load it into a model trainer
            prev_model_obj = self.lolpop.resource_version_control.get_model(
                prev_experiment)
            prev_model = self.lolpop.metadata_tracker.load_model(
                prev_model_obj, self.model_version, self.model)

            #compare model to the last version
            report, file_path = self.lolpop.model_checker.calculate_model_drift(
                self.data_dict, self.model, prev_model)
            self.lolpop.metadata_tracker.log_artifact(
                self.model_version, id="model_drift_report", path=file_path, external=False)
            is_new_model_better = self.lolpop.model_checker.compare_models(
                self.data_dict, self.model, prev_model, self.model_version, prev_model_version)

        else:
            self.log("No previous model version found for model: %s" %
                     self.metadata_tracker.get_resource_if(self.model_version))
            is_new_model_better = True 

        self.is_new_model_better = is_new_model_better
          
        self.next(self.retrain_model_on_all_data)

    @step
    def check_model_bias(self):
        #check model bias
        self.lolpop.model_bias_checker.check_model_bias(
            self.data_dict, self.model, self.model_version)
        
        self.next(self.compare_models)

    @step
    def retrain_model_on_all_data(self):

        #only retrain if the new model is better than last model and 
        #retrain_all config is set
        if self.is_new_model_better: 
            if self.lolpop._get_config("retrain_all"): 
                if hasattr(self.lolpop, "model_trainer"):
                    model, experiment = self.lolpop.model_trainer.rebuild_model(
                        self.data, self.model_version)
                else:
                    #if no model_trainer is specified in config, we can rebuild using the winning_exp_model_trainer
                    winning_exp_model = self.lolpop.metadata_tracker.load_model(
                        None, self.model_version, ref_model=None)
                    model, experiment = winning_exp_model.rebuild_model(
                        self.data, self.model_version)
                self.model = model 

        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == '__main__':
    #need to use CLI here because metaflow calls back into this function to
    #execute each individual step
    MetaflowOfflineTrainSpec(use_cli=True)
