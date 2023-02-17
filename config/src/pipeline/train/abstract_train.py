from pipeline.abstract_pipeline import AbstractPipeline 
from utils import common_utils as utils

class AbstractTrain(AbstractPipeline): 
    def __init__(self, conf, runner_conf, pipeline_type = "train", **kwargs):
        super().__init__(conf, runner_conf, pipeline_type = pipeline_type, **kwargs)

    def split_data(self, data, *args, **kwargs): 
        pass 

    def train_model(self, data, *args, **kwargs): 
        pass 

    def analyze_model(self, *args, **kwargs): 
        pass 

    def check_model(self, *args, **kwargs):
        pass

    def compare_models(self, *args, **kwargs):
        pass

    def deploy_model(self, *args, **kwargs):
        pass

    def load_model(self, model_obj, model_version, ref_model, *args, **kwargs):
        model_trainer = self.metadata_tracker.get_metadata(model_version, "winning_experiment_model_trainer").get("winning_exp_model_trainer")
        model_cl = utils.load_class(model_trainer)
        dependent_components = {"logger" : self.logger, "notifier" : self.notifier,  "metadata_tracker" :self.metadata_tracker, "metrics_tracker": self.metrics_tracker, "resource_version_control": self.resource_version_control}
        model = model_cl(ref_model.config, self.config, self.runner_conf, parent_process=ref_model.parent_process, problem_type = self.problem_type, params=ref_model.params, components=dependent_components) 
        #if you passed in a model_obj, we assume you have a pre-trained model object you wish to use
        if model_obj is not None: 
            model._set_model(model_obj)
        return model
