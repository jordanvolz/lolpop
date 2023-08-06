from lolpop.component.base_component import BaseComponent
from omegaconf.listconfig import ListConfig
from lolpop.utils import common_utils as utils
import itertools 

from typing import Any 

class BaseHyperparameterTuner(BaseComponent): 
    __REQUIRED_CONF__ = {
        "components": ["metadata_tracker", "resource_version_control", "metrics_tracker"],
        "config" : ["training_params", "metrics", "perf_metric"],
    }
    
    def run_experiment(self, data, *args, **kwargs) -> Any: 
        pass 

    def build_model(self, data, model_version, algo, params, trainer_config={}, *args, **kwargs) -> tuple[Any, Any]: 
        #create experiment and log params
        experiment = self.metadata_tracker.create_resource(id=None, type="experiment", parent=model_version)

        #load model trainer and build model
        model_cl = utils.load_class(algo)
        dependent_components = {"logger" : self.logger, "notifier" : self.notifier,  "metadata_tracker" :self.metadata_tracker, "metrics_tracker": self.metrics_tracker, "resource_version_control": self.resource_version_control}
        model = model_cl(conf=trainer_config, pipeline_conf=self.pipeline_conf, runner_conf=self.runner_conf, 
                         parent_process = self.name, problem_type = self.problem_type, params=params, components=dependent_components) 
        model_obj = model.fit(data)

        return model, experiment 

    def save_model(self, model, experiment, params, algo, *args, **kwargs):
        model_obj = model._get_model()
        #save model
        vc_info = self.resource_version_control.version_model(experiment, model_obj, algo=algo)
        experiment_metadata = {
            "training_params" : params,
            "model_trainer" : algo, 
        }
        self.metadata_tracker.register_vc_resource(experiment, vc_info, additional_metadata = experiment_metadata)

        experiment_id = self.metadata_tracker.get_resource_id(experiment, type="experiment")
        model_artifacts = model.get_artifacts(experiment_id) or {}
        for k,v in model_artifacts.items(): 
            self.metadata_tracker.log_artifact(experiment, k, v)

    #builds a grid of all possible parameter combinations gives a params item with a list of values for each param
    def _build_training_grid(self, params) -> dict[str, Any]: 
        keys, values = zip(*params.items())
        values = [v if isinstance(v, ListConfig) else str(v).split(",") for v in values]
        grid = [dict(zip(keys,v)) for v in itertools.product(*values)]

        return grid

    #determines the winning experiment from the experiment list 
    def _get_winning_experiment(self, exp_list, reverse=False) -> Any: 
        # sort list by values. reverse=True is descending, False is ascending (Default)
        new_list = sorted(exp_list.items(), key=lambda x: x[1], reverse=reverse) 
        return new_list[0][0]