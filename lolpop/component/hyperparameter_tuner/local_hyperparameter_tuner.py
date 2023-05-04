from lolpop.component.hyperparameter_tuner.base_hyperparameter_tuner import BaseHyperparameterTuner
from lolpop.utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class LocalHyperparameterTuner(BaseHyperparameterTuner): 

    def run_experiment(self, data, model_version, *args, **kwargs): 
    # params can call different algos and user hyperparam tuning, etc 
    # first we generate a list of experiments + scores    
        exp_list = {}
        model_list = {}
        training_params = self._get_config("training_params")
        metrics = self._get_config("metrics")
        perf_metric = self._get_config("perf_metric")
        for algo in training_params: 
            grid = self._build_training_grid(training_params[algo])
            for params in grid:
                #train model 
                model, experiment = self.build_model(data, model_version, algo, params)
                #save model
                self.save_model(model, experiment, params, algo)
                #make predictions
                predictions = model.predict(data)
                #calculate metrics
                metrics_val = model.calculate_metrics(data, predictions, metrics)
                #log metrics
                self.metrics_tracker.log_metrics(experiment, metrics_val, perf_metric)
                #build experiment list
                exp_id = self.metadata_tracker.get_resource_id(experiment)
                exp_list[exp_id] = metrics_val["valid"][perf_metric]
                model_list[exp_id] = model

        #save data splits
        for k,v in data.items(): 
            vc_info = self.resource_version_control.version_data(model_version, v, key=k)
            self.metadata_tracker.register_vc_resource(model_version, vc_info, key=k, file_type="csv")

        #now, we determine overall best experiment and save into model_version
        winning_exp_id = self._get_winning_experiment(exp_list, perf_metric, reverse=utils.get_metric_direction(perf_metric))
        winning_exp = self.metadata_tracker.get_resource(winning_exp_id, parent=model_version, type="experiment")
        winning_exp_model_trainer = self.metadata_tracker.get_metadata(winning_exp, id="model_trainer")
        best_model = model_list.get(winning_exp_id)

        #log important stuff to model version
        self.metrics_tracker.copy_metrics(winning_exp, model_version)
        self.metadata_tracker.log_metadata(model_version, id="winning_experiment_id", data={"winning_experiment_id" : winning_exp_id})
        self.metadata_tracker.log_metadata(model_version, id="winning_experiment_model_trainer", data={"winning_experiment_model_trainer" : winning_exp_model_trainer})

        return best_model