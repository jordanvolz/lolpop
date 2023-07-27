## Overview

A `model_checker` is a component that takes a model and runs checks on that model. These models checks are typically concerned with things like model error, overfitting, baseline comparisons, drift, etc.  

`BaseModelChecker` exposes two main methods for children to implement: `check_model` and `calculate_model_drift`. Additionally, it implements its own baseline comparison method. 

## Attributes

`BaseModelChecker` contains no default attributes. 

## Configuration

`BaseModelChecker` contains the following required components: 

- `metrics_tracker`

`BaseModelChecker` contains the following required configuration: 

- `baseline_method`: The baseline method to use for baseline comparisons. Possible values for `baseline_method` are `column` and `value`. 
- `baseline_value`: The value of the baseline method to use. If `baseline_method` is `column` then `baseline_value` should be the name of the column to use as the baseline. This scenario is designed for user-defined baselines. I.E. you can create whatever baseline you wish and put it as a separate column. If `baseline_method` is `value` then the following are accepted for `baseline_value`: 
    - `problem_type`: `classification`
        - `class_avg`: randomly selects class based on the frequency they appear in the provided dataset. 
        - `class_most_frequent`: selects the most prominent class
    - `problem_type`: `regression`
        - `avg`: selects the average value
        - `mode`: selects the mode
        - `max`:  selects the max value
        - `min`: selects the min value
        - `median`: selects the median value
    - `problem_type`: `timeseries`
        - `last_value`: selects the previous value
        - `lag_mean`: selects the mean over a window
        - `lag_max`: selects the max over a window
        - `lag_min`: selects the min over a window
        - `lag_median`: selects the median over a window
        - for all `lag_` `baseline_values` you can specify the window via `lag_mean_X`, where `X` is the number of rows to use in the window. I.E. `lag_mean_7` takes the mean over the last 7 values. 
- `perf_metric`: The performance metric used to determine if 

## Interface

The following methods are part of `BaseModelChecker` and should be implemented in any class that inherits from this base class: 

### check_model

Performs a model check on the given model. 

```python
def check_model(self, data, model, *args, **kwargs) -> tuple[Any, str, str]
```

**Arguments**: 

- `data` (dict): A dictionary of train/test data.  
- `model` (object): The model to check.

**Returns**:

- `model_report` (Any): Python object of the model report.
- `file_path` (string): Path to the exported report.
- `checks_status` (string): Status of the checks ("PASS"/"WARN"/"ERROR", etc.)

### calculate_model_drift

Performs a drift comparison between two models.

```python
def calculate_model_drift(self, data, model, deployed_model, *args, **kwargs) -> tuple[Any, str]
```

**Arguments**: 

- `data` (dict): A dictionary of train/test data.  
- `model` (object): The model to check. 
- `deployed_model` (object): The currently deployed model. 

**Returns**:

- `model_report` (Any): Python object of the model report.
- `file_path` (string): Path to the exported report.

## Default Methods

The following are default methods that are implemented in the base class. They can be overridden by inheriting classes as needed.

### get_baseline_comparison
Compare the model performance against a baseline.

```python
def get_baseline_comparison(self, data, model, model_version, *args, **kwargs) -> tuple[bool, float]
```

        

**Argumentss**:
    
- `data` (dict): The data for model evaluation.
- `model` (obj): The trained model object.
- `model_version` (obj): The model version object, obtained from a `metadata_tracker`.
 
**Returns**:
    
- (bool) Is the baseline better than the model?
- (float) The metric difference between the model and the baseline.

### compare_models

Compare the performance of the current model against the previous model.

```python
compare_models(self, data, model, prev_model, model_version, prev_model_version=None, *args, **kwargs) -> bool
```
**Argumentss**:

- `data` (dict): The data for model evaluation.
- `model` (object): The current trained model object.
- `prev_model` (object): The previous trained model object.
- `model_version` (object): The version of the current model.
- `prev_model_version` (object): The version of the previous model (default None).

**Returns**:

- `bool`: True if the current model is better than the previous model, False otherwise.


### _get_baseline_predictions

Get baseline predictions based on the baseline method and value.

```python
def _get_baseline_predictions(self, data, baseline_method, baseline_value, *args, **kwargs) -> dict[str,Any]
```
**Arguments**:

- `data` (dict): The data for baseline comparison.
- `baseline_method` (str): The method for baseline comparison.
- `baseline_value` (str): The value used in baseline comparison.

**Returns**:
    
- `dict`: A dictionary containing the baseline predictions for different data splits.

### _get_metric_comparison

Compares two metric values and determines which is better. 

```python
def _get_metric_comparison(self, champion_metric, challenger_metric, perf_metric, *args, **kwargs) -> tuple[bool, float]
```
**Argumentss**:

- `champion_metric` (dict): champion metric
- `challenger_metric` (dict): challenger metric
- `perf_metric` (str): The performance metric to use to determine which metric is best

**Returns**:

- `bool`: is the challenger metric better? True or False 
- `float`: difference between champion and challenger metric

### _compare_model_performance

Compares model performance to deployed model against a static data set. 

```python 
def _compare_model_performance(self, model, deployed_model, data, perf_metric, current_model_version, *args, **kwargs) -> tuple[bool, float]
```

**Arguments**:
    
- `model` (object): current model
- `deployed_model` (object): deployed model
- `data` (dictionary): dicitonary of training/test data
- `perf_metric` (str): performance metric to use to determine which model is better
- `current_model_version` (object): current model verison to log metrics into

**Returns**:

- `bool`: Is the new model better? True or False
- `float`: difference between metric values