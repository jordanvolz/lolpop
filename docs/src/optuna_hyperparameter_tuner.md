## OptunaHyperparameterTuner Class

The `OptunaHyperparameterTuner` class is a subclass of `BaseHyperparameterTuner`, used for optimizing model hyperparameters using the Python library `Optuna`.

### Methods

* `run_experiment(data, model_version, n_trials=100, *args, **kwargs)`: This method is used to optimize the algorithm hyperparameters using `Optuna`. `data` represents the dataset to train the model, `model_version` represents the object version from the metadata tracker, and `n_trials` represents the number of trials to run, with the default value being 100. The method returns the best generated model as an object.

* `_optuna_objective(trial, param_type, data, model_version, algo, params, trainer_config, metrics, perf_metric, experiment_list, model_list)`: This is the objective function for `Optuna` optimization. It takes a `trial` object and a number of other parameters and returns the value of the specified performance metric.

* `_parse_dynamic_logic(trial, name, p)`: This method is used to parse each value of a dynamic configuration to the `Optuna` type. It takes a `trial` object, the name of the configuration parameter, and a dictionary containing the value, type, and range of the parameter. The method returns the parsed value.

* `_get_dynamic_params(trial, params)`: This method retrieves the parameters corresponding to the dynamic type of parameter tuning. It takes a `trial` object and a dictionary of parameters, and returns a dictionary containing the generated parameters.

* `_get_fixed_params(trial, params)`: This method retrieves the parameters corresponding to the fixed type of parameter tuning. It takes a `trial` object and a dictionary of parameters, and returns a dictionary containing the generated parameters.

* `_log_trial(trial, model_params, model, experiment, algo)`: This method is used to log the trial run, the generated model, and the parameters. It takes a `trial` object, a dictionary of generated parameters, the generated model, the experiment used to train the model, and the name of the algorithm being used for training. The method returns the experiment used to train the model.

* `_log_study(study, model_version, algo)`: This method is used to save interesting parts of the study containing the optimization history, which can be referred to later. It takes a `study` object, a model version object from the metadata tracker, and the name of the algorithm being used for training.

* `_save_plot(name, plot, model_version, algo)`: This method is used to save an HTML plot containing the `Optuna` optimization history to disk. It takes a name for the saved HTML file, an object containing the plot data, a model version object from the metadata tracker, and the name of the algorithm being used for training. The method returns an instance of the `Artifact` class corresponding to the saved plot.

### Example

```
import OptunaHyperparameterTuner

# create a new instance of OptunaHyperparameterTuner
tuner = OptunaHyperparameterTuner()

# define dataset
data = {"train": train_data, "valid": valid_data}

# define model version object from metadata tracker
model_version = metadata_tracker.get_resource("model_version_id")

# optimize hyperparameters using Optuna
best_model = tuner.run_experiment(data, model_version, n_trials=100)
```