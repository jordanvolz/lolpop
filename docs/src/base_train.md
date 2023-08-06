## Overview

The `train` pipeline is a pipeline that performs common model training activities, such as performing a grid search, versioning models, computing feature importance, checking for model bias, etc. 

## Attributes

`BaseTrain` contains no default attributes.

## Configuration

`BaseTrain` contains no default or required configuration. 


## Interface

The following methods are part of `BaseTrain` and should be implemented in any class that inherits from this base class: 

### split_data

Splits the input data into a dictionary containing training/test/validation data. 

```python
def split_data(self, data, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): The data to split


**Returns**:

- `data_dict` (dict): The split data.


### train_model

Trains a model. 

```python
def train_model(self, data, *args, **kwargs) -> tuple[Any, Any]
```

**Arguments**: 

- `data` (object): The dictionary of train/test/validation data. 

**Returns**:

- `model` (object): The trained model 
- `model_version` (object): The model version object created by versioning the model. 


### check_model

Runs model checks on a model. 

```python
def check_model(self, data, model, model_version, *args, **kwargs)
```

**Arguments**: 

- `data` (object):  The dictionary of train/test/validation data.
- `model` (object): The trained model 
- `model_version` (object): The model version object created by versioning the model. 

**Returns**:

Nothing 

### analyze_model

Runs various model analysis, such as feature importance, baseline comparison, confusion matrix, error plots, etc. Analysis will vary by problem type. 

```python
def analyze_model(self, data, model, model_verison, *args, **kwargs)
```

**Arguments**: 

- `data` (object):  The dictionary of train/test/validation data.
- `model` (object): The trained model 
- `model_version` (object): The model version object created by versioning the model. 

**Returns**:

Nothing

### compare_models

Runs a model drift analysis and generates a drift report. 

```python
def compare_models(self, data, model, model_version, *args, **kwargs) -> bool
```

**Arguments**: 

- `data` (object):  The dictionary of train/test/validation data.
- `model` (object): The trained model 
- `model_version` (object): The model version object created by versioning the model. 

**Returns**:

- `is_new_model_better` (bool): Whether or not the current model version performs better than the deployed version. 

### check_model_bias

Runs model bias checks and logs bias metrics. 

```python
def check_model_bias(self, data, model, model_version, *args, **kwargs)
```

**Arguments**: 

- `data` (object):  The dictionary of train/test/validation data.
- `model` (object): The trained model 
- `model_version` (object): The model version object created by versioning the model. 

**Returns**:

Nothing. 

### retrain_model_on_all_data

Runs model bias checks and logs bias metrics. 

```python
def retrain_model_on_all_data(self, data, model_version, *args, **kwargs) -> tuple[Any, Any]
```

**Arguments**: 

- `data` (object):  The dictionary of train/test/validation data.
- `model_version` (object): The model version object created by versioning the model. 

**Returns**:

- `model` (object): The newly trained model. 
- `experiment` (object): The experiment the model was trained in. 

