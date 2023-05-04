from lolpop.component.hyperparameter_tuner.base_hyperparameter_tuner import BaseHyperparameterTuner
from lolpop.utils import common_utils as utils
import optuna
from datetime import datetime
import os

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class OptunaHyperparameterTuner(BaseHyperparameterTuner): 

    def run_experiment(self, data, model_version, n_trials=100, timeout=600, *args, **kwargs): 
        #set up params
        training_params = self._get_config("training_params")
        param_type = self._get_config("param_type", "fixed")
        metrics = self._get_config("metrics")
        perf_metric = self._get_config("perf_metric")

        #understand if we want to minimize or maximum objective for optuna
        reverse = utils.get_metric_direction(perf_metric)
        direction = "maximize"
        if reverse: 
            direction = "minimize"
            
        exp_list = {} 
        model_list = {}
        for algo in training_params: 
            #need to create study w/ sampler so that the results are reproducible later on
            sampler = optuna.samplers.TPESampler(seed=42) 
            study_name = self.metadata_tracker.get_resource_id(model_version)
            study = optuna.create_study(direction=direction, sampler=sampler, study_name=study_name)
            if param_type == "fixed":
                grid = self._build_training_grid(training_params[algo])
                #enqueue all fixed params
                for params in grid: 
                    study.enqueue_trial(params)   
                #only run n_trials = len(grid) to only run enqued params
                n_trials = len(grid)
            #run study
            study.optimize(lambda trial: self._optuna_objective(trial, param_type, data, model_version, algo, training_params[algo], metrics, perf_metric, exp_list, model_list), n_trials=n_trials, timeout=timeout)
            #log study
            #study.set_user_attr("perf_metric_name", perf_metric)
            #study.set_user_attr("perf_metric_val", study.best_value)
            self._log_study(study, model_version, algo) #returns best exp id 
            #get best experiment in study
            #best_experiment = study.best_trial.user_attrs.get("experiment_id")
            #exp_model = study.best_trial.user_attrs.get("model")
            #exp_list[best_experiment] = study.best_value
            #model_list[best_experiment] = exp_model 

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
        self.metadata_tracker.log_metadata(model_version, id="winning_experiment_id", data=winning_exp_id)
        self.metadata_tracker.log_metadata(model_version, id="winning_experiment_model_trainer", data=winning_exp_model_trainer)
      
        return best_model

    def _optuna_objective(self, trial, param_type, data, model_version, algo, params, metrics, perf_metric, experiment_list, model_list): 
        #if we are dynamic we just need to modify the paramst to use suggest_x to dynamically create values 

        if param_type == "dynamic": 
            model_params = self._get_dynamic_params(trial, params)
        else: #param_type=="fixed"
            model_params = self._get_fixed_params(trial, params)
        #build model
        model, experiment = self.build_model(data, model_version, algo, model_params)
        #make predictions
        predictions = model.predict(data)
        #calculate metrics
        metrics_val = model.calculate_metrics(data, predictions, metrics)
        perf_metric_value = metrics_val["valid"][perf_metric]

        #need to save exp model now because optuna doesn't provide access to models objects later on. 
        #use model_params instaed of trial.params as optuna doesn't track fixed parameters, but the user may want to
        self._log_trial(trial, model_params, model, experiment, algo)
        #log metrics
        self.metrics_tracker.log_metrics(experiment, metrics_val, perf_metric)

        #save experiment id and model so we can refer back to it later 
        #note, for large models this may cause memory issues!
        experiment_id = self.metadata_tracker.get_resource_id(experiment)
        experiment_list[experiment_id] = perf_metric_value
        model_list[experiment_id] = model
        
        #clean up resource
        self.metadata_tracker.clean_resource(experiment, type="experiment")

        #objective function needs to return perf value for so optuna can do comparison
        return perf_metric_value

    # parses each value of a dynamic config to the optuna type
    def _parse_dynamic_logic(self, trial, name, p):
        param_type = p.get("type")

        if param_type == "fixed": 
            return p.get("value")
        elif param_type == "int": 
            low_high = p.get("range")
            return trial.suggest_int(name, low_high[0], low_high[1])
        elif param_type == "float":
            low_high = p.get("range")
            return trial.suggest_float(name, low_high[0], low_high[1])
        elif param_type == "categorical":
            choices = p.get("choices")
            return trial.suggest_categorical(name, choices)

    def _get_dynamic_params(self, trial, params):
        params_out = {}
        for p in params: 
            params_out[p] = self._parse_dynamic_logic(trial, p, params[p])
        return params_out

    def _get_fixed_params(self, trial, params): 
        params_out = {}
        for p in params: #since the params passed for a fixed set are static, we can represent them as a categorical
            params_out[p] = trial.suggest_categorical(p, params[p])
        return params_out

    def _log_trial(self, trial, model_params, model, experiment, algo):
        #log params + trainer
        self.metadata_tracker.log_metadata(experiment, id="optuna_trial_number", data=trial.number)
        self.metadata_tracker.update_resource(experiment, {"start_time": trial.datetime_start, "end_time":datetime.utcnow()})
        
        #save model
        self.save_model(model, experiment, model_params, algo)

        return experiment

    #saves interesting parts of the study
    def _log_study(self, study, model_version, algo): 
        if optuna.visualization.is_available(): 
            plot = optuna.visualization.plot_edf(study)
            self._save_plot("optuna_plot_edf.html",plot, model_version,algo)

            #only useful if using intermediate values and pruning
            #plot = optuna.visualization.plot_intermediate_values(study)
            #self._save_plot("optuna_plot_intermediate_values.html",plot, model_version,algo)

            plot = optuna.visualization.plot_optimization_history(study)
            self._save_plot("optuna_plot_optimization_history.html",
                            plot, model_version, algo)

            plot = optuna.visualization.plot_parallel_coordinate(study)
            self._save_plot("optuna_plot_parallel_coordinate.html",
                            plot, model_version, algo)

            plot = optuna.visualization.plot_param_importances(study)
            self._save_plot("optuna_plot_param_importances.html",
                            plot, model_version, algo)

            #only used for multi-objective studies
            #optuna.visualization.plot_pareto_front(study)
            #self._save_plot("optuna_plot_pareto_front.html",plot, model_version,algo)

            plot = optuna.visualization.plot_slice(study)
            self._save_plot("optuna_plot_slice.html",
                            plot, model_version, algo)

            plot = optuna.visualization.plot_contour(study)
            self._save_plot("optuna_plot_contour.html",
                            plot, model_version, algo)
    
    #saves plot 
    def _save_plot(self, name, plot, model_version, algo): 
        name_arr = name.split(".")
        plot_type = name_arr[-1]
        plot_name = "_".join(name_arr)

        local_path = "%s/%s/%s" %(
            self._get_config("local_dir"), 
            self.metadata_tracker.get_resource_id(model_version),
            algo
            )
        os.makedirs(local_path, exist_ok=True)
        local_file = "%s/%s" %(local_path, name)
        plot.write_html(local_file)
        artifact = self.metadata_tracker.log_artifact(model_version, id = plot_name, path = local_file, mime_type = plot_type, external = False)

        return artifact