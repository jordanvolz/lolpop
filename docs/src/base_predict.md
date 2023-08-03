## Overview

The `predict` pipeline is a pipeline that performs common actions concerning predictions, such as making predictions from new data, versioning predictions, and analzing predictions.

## Attributes

`BasePredict` contains no default attributes. 

## Configuration

`BasePredict` contains no default or required configuration. 


## Interface

The following methods are part of `BasePredict` and should be implemented in any class that inherits from this base class: 

### compare_data

Compares the prediction dataset to another dataset, such as the training dataset. The intestion here is to capture data skew from training time to prediction time. 

```python
def compare_data(self, model_version, dataset_version, data, *args, **kwargs)
```

**Arguments**: 

- `model_version` (object): The model version object that is being promoted.  
- `dataset_version` (object): The dataset version object containing to old data to compare the prediction data to. 
- `data` (object): The prediction data. 

**Returns**:

Nothing

### get_predictions

Runs a prediciton job to get predictions from a new dataset

```python
def get_predictions(self, model, model_version, data, *args, **kwargs) -> tuple[Any, Any]
```

**Arguments**: 

- `model` (object): The model object to use to make predictions. 
- `model_version` (object): The model version containing the model
- `data` (object): The prediction data

**Returns**:

- `predictions` (object): The predictions
- `prediction_job` (object): The prediction job that created the predictions, created from a `metadata_tracker`

### track_predictions

Versions the results of a prediction job.

```python
def track_predictions(self, prediction_job, data, *args, **kwargs)
```

**Arguments**: 

- `prediction_job` (object): The prediction job from the `metadata_tracker`
- `data` (object): The predictions. 

**Returns**:

Nothing 

### analyze_prediction_drift

Analyzes drift between the current predictions and the previously produced predictions. 

```python
def analyze_prediciton_drift(self, dataset_version, prediction_job, data, *args, **kwargs)
```

**Arguments**: 

- `dataset_version` (object): The dataset_version corresponding to the current predictions. 
- `predition_job` (object): The prediction job that created the predictions.  
- `data`: (object): The prediction data. 

**Returns**:

Nothing

### check_predictions

Runs prediction checks. 

```python
def check_predictions(self, data, prediction_job,  *args, **kwargs)
```

**Arguments**: 

- `data` (object): The predictions
- `predition_job` (object): The prediction job that created the predictions.  

**Returns**:

Nothing

### save_predictions

Save predictions.  

```python
def save_predictions(self, data, target, *args, **kwargs)
```

**Arguments**: 

- `data` (object): The predictions
- `target` (str): The place to save the predictions. Could be a local file, path in an object store, or a table in a data warehouse, etc. 

**Returns**:

Nothing
