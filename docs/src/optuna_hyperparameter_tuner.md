# OptunaHyperparameterTuner

The `OptunaHyperparameterTuner` class is a subclass of `BaseHyperparameterTuner`, used for optimizing model hyperparameters using the Python library `Optuna`.

## Configuration 

### Required Configuration 

In addition to the required configuration in the [BaseHyperparameterTuner](base_hyperparameter_tuner.md), `OptunaHyperparamterTuner` also requires the following: 

- `local_dir`: A local directory to use during operation. 

### Default Configuration 

`OptunaHyperparamterTuner` uses the following default configuration: 

- `param_type`: The parameter type used in the `training_params` configuration. Default is "fixed". "dynamic" is also accepted.  
- `optuna_timeout`: The maximum amount of time to run experiments before gracefully exiting. Default is 3600 (i.e. one hour).  
- `num_jobs`: The number of concurrent experiments to run in Optuna. Defaults to 1. 
- `num_trials`: The maximum number of trials to run. Only used if `param_type` is "dynamic". otherwise, `num_trails` is equal to the length of the parameter grid. Deafaults to 100.  
## Methods

### run_experiment 
This method is used to optimize the algorithm hyperparameters using `Optuna`. This runs an Optuna study and will select the best experiment (i.e. Optuna *trial*) created during the study run time. 

 ```python 
 run_experiment(data, model_version, *args, **kwargs)
 ```  
 **Arguments**: 

-  `data` (object): represents the dataset to train the model, 
- `model_version` (object): represents the object version from the metadata tracker, 

**Returns**: 

-The best generated model as an object.

### _optuna_objective
This is the objective function for `Optuna` optimization. This should typically not be overridden. 

 ```python 
 def _optuna_objective(trial, param_type, data, model_version, algo, params, trainer_config, metrics, perf_metric, experiment_list, model_list)
 ```
 **Arguments**: 

 - `trial` (object): The `Optuna` trial object. 
 - `param_type` (str): The `param_type` used, either "fixed" or "dynamic". 
 - `data` (object): The data to use for model training and evaluation. 
 - `model_version` (object): The model version object obtained from the `metadata_tracker`. 
 - `algo` (str): The name of the `model_trainer` class to use for this experiment. 
 - `params` (dict): A dictionary of key-value pairs to use for model configuration. 
 - `trainer_config` (dict): A dictionary of key-value pairs to use for the `model_trainer` configuration
 - `metrics` (list): A list of metrics to calculate.
 - `perf_metric` (str): The metric to use to determine the winning experiment. 
 - `exp_list` (dict): A dictionary of completed experiments and their `perf_metric` value. This will be added to with the current experiment.  
 - `model_list` (dict): A dictionary of completed experiments and their model objects. This will be added to with the current experiment. 

**Returns**: 

- The value of the specified performance metric for the trained model.

### _parse_dynamic_logic
This method is used to parse each value of a dynamic configuration to the proper `Optuna` type. 
 

 ```python 
 def _parse_dynamic_logic(self, trial, name, p)
 ``` 
 
 **Arguments**: 

 - `trial` (object): the `Optuna` trial object. 
 - `name` (str): name of the configuration parameter
 - `p` (dict): dictionary containing the type, and value/range/choices of the parameter

 **Returns**: 
 - Returns the parsed value in `Optuna` form. I.E. will return `optuna.suggest_X()` where `X` is based on the input type. 

### _get_dynamic_params
This method retrieves the parameters corresponding to the dynamic type of parameter tuning.

 ```python 
def _get_dynamic_params(self, trial, params)
 ``` 

 **Arguments**: 

- `trial` (object): The `Optuna` trial object. 
- `params` (dict): A dictionary of parameter values. 

 **Returns**: 
- A dictionary containing the generated parameters. (Generated via `_parse_dynamic_logic`)

### _get_fixed_params
This method retrieves the parameters corresponding to the fixed type of parameter tuning.

```python 
def  _get_fixed_params(self, trial, params)
```  
 
 **Arguments**: 

- `trial` (object): The `Optuna` trial object. 
- `params` (dict): A dictionary of parameter values. 


**Returns**: 

A dictionary containing the generated parameters.

### _log_trial
This method is used to log the trial run, the generated model, and the parameters. 


 ```python 
 def _log_trial(self, trial, model_params, model, experiment, algo)
 ``` 
 It takes a `trial` object, a dictionary of generated parameters, the generated model, the experiment used to train the model, and the name of the algorithm being used for training. The method returns the experiment used to train the model.

 **Arguments**: 

- `trial` (object): The `Optuna` trial object. 
- `model_params` (dict): A dictionary of parameter values. 
- `model` (object): The model object.
- `experiment` (object): The experiment object obtained from the `metadata_tracker`. 
- `algo` (str): The name of the `model_trainer` class to use for this experiment.  

**Returns**: 
- The (possibly updated) experiment object. 

### _log_study
This method is used to save interesting parts of the study containing the optimization history, which can be referred to later.

 ```python 
 def _log_study(self, study, model_version, algo)
 ```  

**Arguments**: 
- `study` (object): The `Optuna` study object. 
- `model_version` (object): The model version object to log the study into.
- `algo` (str): The name of the `model_trainer` class used for this experiment.  

## _save_plot
 This method is used to save an HTML plot containing the `Optuna` optimization history to disk. 

 ```python 
 _save_plot(self, name, plot, model_version, algo)
 ``` 

 **Arguments**: 

 - `name` (str): A name for the saved HTML file
 - `plot` (object): The `Optuna` plot
 - `model_version` (object): The model version object to save the plot into, obtained from the `metadata_tracker` 
 - `algo` (str): The name of the `model_trainer` class used for this experiment.  

**Returns**: 

An instance of the `Artifact` class corresponding to the saved plot.

## Usage

```python
from lolpop.component import OptunaHyperparameterTuner, LocalDataSplitter, MLFlowMetadataTracker
import pandas as pd 

#get data
data_splitter_config = {
    #insert component config
} 
data_splitter = LocalDataSplitter(conf=data_splitter_config)
df = pd.read_csv("/path/to/data.csv")
data = data_spliter.split_data(df)

#get model_version
metadata_tracker_config = {
    #insert component config here
}
metadata_tracker = MLFlowMetadataTracker(conf=config)
model_version = metadata_tracker.create_resource(id, type="model_version")

config = {
    #insert component config here 

}
# create an instance of LocalHyperparameterTuner
oht = OptunaHyperparameterTuner(conf=config)

# run the experiment
best_model = oht.run_experiment(data, model_version)
``` 

### Sample training parameters

#### Fixed

```yaml 
  hyperparameter_tuner: 
    config: 
      param_type: fixed
      training_params: 
        XGBoostModelTrainer: 
          objective: ["multiclass"]
          max_depth: [4,8]
          alpha: [1,5,10]
          learning_rate: [1.0]
          n_estimators: [10]
          random_state: [0]
```

#### Dynamic

```yaml
  hyperparameter_tuner: 
    config: 
      param_type: dynamic
      training_params: 
        XGBoostModelTrainer: 
          objective: {"type": "categorical", "choices" : ["multiclass"]}
          max_depth: {"type": "int", "range" : [4,8]}
          alpha: {"type": "float", "range" : [1,10]}
          learning_rate: {"type": "float", "range" : [0.1,1]}
          n_estimators: {"type": "int", "range" : [1,10]}
          random_state: {"type": "fixed", "value" : 0}

```