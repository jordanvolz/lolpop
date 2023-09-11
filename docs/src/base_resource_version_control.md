## Overview

A `resource_version_control` is a component that is able to version control resources in the machine learning workflow, such as datasets and machine learning models. A `resource_version_control` system is able to save resources to persistent storage as well as retrieve those items in the future. 


## Attributes

`BaseResourceVersionControl` contains no default attributes. 

## Configuration

`BaseResourceVersionControl` contains no default or required configuration. 


## Interface

The following methods are part of `BaseResourceVersionControl` and should be implemented in any class that inherits from this base class: 

### version_data

Versions a dataset.   

```python
def version_data(self, dataset_version, data, *args, **kwargs) -> dict[str, Any]
```

**Arguments**: 

- `dataset_version` (object): The dataset version being versioned
- `data` (object): The data to version

**Returns**: 

- `dict`: Attributes returned from the resource version control system, such as a commit hash. The returned information should be able to be used to retrieve the object in the future and may very likely be logged in the `metadata_tracker`



### get_data

Versions a dataset.   

```python
def get_data(self, dataset_version, *args, **kwargs) -> Any 
```

**Arguments**: 

- `dataset_version` (object): The dataset version  to retrieve data from


**Returns**: 

- `data`: The data of the object

### version_model

Versions a model.   

```python
def version_model(self, experiment, model, *args, **kwargs) -> dict[str, Any]
```

**Arguments**: 

- `experiment` (object): The experiment being verisoned
- `model` (object): The model to version

**Returns**: 

- `dict`: Attributes returned from the resource version control system, such as a commit hash. The returned information should be able to be used to retrieve the object in the future and may very likely be logged in the `metadata_tracker`

### get_model

Returns a model object from an experiment.   

```python
def get_model(self, experiment, *args, **kwargs) -> Any
```

**Arguments**: 

- `id` (str): The experiment to retrieve the model from

**Returns**: 

- `model`: The model object from the experiment. 


### version_feature_transformer

Versions a feature transformer.   

```python
def version_feature_transformer(self, experiment, transformer, *args, **kwargs) -> dict[str, Any]
```

**Arguments**: 

- `experiment` (object): The experiment being verisoned
- `transformer` (object): The feature transformer to version

**Returns**: 

- `dict`: Attributes returned from the resource version control system, such as a commit hash. The returned information should be able to be used to retrieve the object in the future and may very likely be logged in the `metadata_tracker`

### get_feature_transformer

Returns a feature transformer object from an experiment.   

```python
def get_feature_transformer(self, experiment, *args, **kwargs) -> Any
```

**Arguments**: 

- `experiment` (object): The experiment to retrieve the feature_transformer from

**Returns**: 

- `feature_transformer`: The feature transformer object from the experiment. 