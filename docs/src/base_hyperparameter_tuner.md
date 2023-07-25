## Overview

A `hyperparameter_tuner` is a component that is able to run many experiments over different `model_trainer` classes. The intention of the component is to provided a standardized way for data scientists to run experiments, track all progress, and streamline evaluating and determining winning experiments. 

Users can provide a grid of `model_trainers` and parameters to run on a given dataset, which will prompt building multiple experiments for each the specified parameters and `model_trainers`. 

## Attributes

`BaseHyperparameterTuner` contains no default attributes. 

## Configuration

### Required Configuration 

`BaseHyperparameterTuner` has the following required components:

- `metadata_tracker`
- `resource_version_control`
- `metrics_tracker`

`BaseHyperparameterTuner` has the following required configurations: 

- `training_params`: A dictionary of `model_trainer` classes and associated configuration, in the form `{<ModelTrainerClass>: {<key>:<value>, ...}, ... }`
- `metrics`: A list of metrics to evaluate for any experiment. 
- `perf_metric`: The metric designated as the "performance metric". I.E. the experiment with the best performance relative to this metric will be considered the winning experiment. 
 


## Interface

The following methods are part of `BaseHyperparameterTuner` and should be implemented in any class that inherits from this base class: 

### run_experiment

This method runs an experiment set on a grid of `model_trainer` classes and associated parameters. If you are writing your own hyperparameter tuner, it is expected that this is the main class that you would implement. It would be expected that you would additionally leverage the `build_model` method below for each experiment, either by using the default implementation or implementing your own. 

```python
def run_experiment(self, data, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): The data object to use to train models in the experiment set. This should be the output of a `data_splitter`.`split_data` method.   

**Returns**:

- `model` (object): This returns the best model in the experiment. 

## Default Methods

The following are default methods that are implemented in the base class. They can be overridden by inheriting classes as needed. 

### build_model

This method runs a single experiment.   

```python
def build_model(self, data, model_version, algo, params, trainer_config={}, *args, **kwargs) -> tuple[Any, Any]
```

**Arguments**: 

- `data` (object): The role you wish the LLM to assume during the conversation. 
- `model_version` (object): The model version object associated with the model that will be created by this method. This should come from a `metadata_tracker` component. 
- `algo` (str): The `model_trainer` class to use for training.
- `params` (dict): Training parameters for the `model_trainer` algorithm. 
- `trainer_config` (dict): Configuration parameters for the `model_trainer` class. 

**Returns**:

- `model`: (object) The `model_trainer` object created from the `algo` and `trainer_config`.
- `experiment`: (object) The experiment object created in the `metadata_tracker` for this experiment. 


### save_model

Version controls and saves the model object and any associated artifacts to the `resource_version_control` system and `metadata_tracker`.

```python
def save_model(self, model, experiment, params, algo, *args, **kwargs)
```

**Arguments**: 

- `model` (object): The model object created during this experiment. 
- `experiment` (experiment): The `metadata_tracker` experiment created for this experiment.  
- `params` (dict): The training parameters used in the experiment
- `algo` (str): The algorithm used in this experiment. 


### _build_training_grid

Helper function that builds a grid of all possible parameter combinations given a `params` item with a list of values for each param. I.E. given input of: 

```python
{
    "key_1": [1],
    "key_2": [1,2],
}
```

We would want the following as output: 

```python
[
    {"key_1": 1, "key_2": 1},
    {"key_1": 1, "key_2": 2},
]
```
The latter can easily be iterated over and passed into our `model_trainer` of choice. 


```python
def _build_training_grid(self, params) -> dict[str, Any]
```

**Arguments**: 

- `params` (dict): The role you wish the LLM to assume during the conversation. 

**Returns**:

- `dict` (str, Any): The training grid with all combinations of parameters. 

### _get_winning_experiment

Helper method that selects the winning experiment from a given dictionary of experiments. The dictionary of experiments should be built during the `run_experiment` method to keep track of all completed experiments and the `perf_metric` of each. 

```python
def _get_winning_experiment(self, exp_list, reverse=False) -> Any
```

**Arguments**: 

- `exp_list` (dict): The dictionary of experiments, in the form of `{"<experiment_id>":<perf_metric_value>}`
- `reverse` (bool): Whether or not to lower values (`False`) or higher values (`True`) are considered better. Defaults to `False` (i.e. lower values are better). 

**Returns**:

- `exp_id` (str): The winning experiment id.
