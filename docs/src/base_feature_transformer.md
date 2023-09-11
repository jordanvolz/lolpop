## Overview

A `feature_transformer` is a component that transforms data into features for a ML model. This is consists of encoding or scaling values to make them better suited for model training. Contrast this with a `data_transformer`, which contains more of a data engineering-style workflow around reshaping or creating new data. 

Feature transformers can either be set at the `train` pipeline level, or at the `model_trainer` component level. If set at the pipeline level, the transformer will apply to every model created in the pipeline (e.g. if you are doing hyperparameter tuning across multiple experiments and wish to use the same transformer for each). Setting a feature transformer at the `model_trainer` level will apply only to that model trainer. This can be useful if you wish to override the pipeline feature transformer for a particular model type. 

## Attributes

`BaseDataConnector` contains no default attributes. 

## Configuration

`BaseDataConnector` contains no the following required components: 

- `metadata_tracker`
- `resource_version_control`


## Interface

The following methods are part of `BaseFeatureTransformer` and should be implemented in any class that inherits from this base class: 

### fit 

```python
def fit(self, data, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): The source data to fit the feature transformer on. This should be something like a local python object (pandas.DataFrame).

**Returns**:

- `transformer` (Any): Returns a fitted feature transformer.


### transform

Transforms data using the feature transformer. 

```python
def transform(self, data, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): The data to transform with the fitted feature transformer. This could be something like a local python object (pandas.DataFrame).

**Returns**:

- `data_out` (Any): Returns a data object, such as a `pandas` Dataframe, which has been transformed by the feature transformer. 

### fit_transform 
Fits the transformer to the provided data, and then transform that data using the fitted feature transformer. 

```python
def fit_transform(self, data, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): The data to fit and transform with the fitted feature transformer. This could be something like a local python object (pandas.DataFrame).

**Returns**:

- `data_out` (Any): Returns a data object, such as a `pandas` Dataframe, which has been transformed by the feature transformer. 


## Default Methods 

The following methods are implemented in the base class. You may find a need to overwrite them as you implement your own feature transformers.
### save 
Saves the feature transformer into a resource version control system. 

```python
def save(self, experiment, *args, **kwargs) -> Any
```

**Arguments**: 

- `experiment` (object): The experiment in which to save the feature transformer. This object should be created by the `metadata_tracker`.

**Returns**:

- Nothing. 
