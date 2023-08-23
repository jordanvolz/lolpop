## Overview

A `model_trainer` is a component that essentially acts as a wrapper around a library that trains a machine learning model. It is expected that this class can `fit` a model to data and also `predict` the values of new data. 


## Attributes

`BaseModelTrainer` contains the following default attributes: 

- `model`: The trained model object. This should get set in the `fit` function. 
- `mlflow_module`: The name of the MLFlow submodule which contains the proper `log_model` method for this trainer. This is only needed if you intend to use MLFlow as your model repository
- `params`: The training parameters for the trained model. 

## Configuration


### Required Configuration 

`BaseModelTrainer` contains the following required components: 

- `metadata_tracker`
- `metrics_tracker`
- `resource_version_control`

and the following required configuration: 

- `metrics`: A list of metrics to compute.
- `perf_metric`: The metric to use for determining which experiment contains the best model. 

## Interface

The following methods are part of `BaseModelTrainer` and should be implemented in any class that inherits from this base class: 

### fit

Fits a model to the provided data. 

```python
def fit(self, data, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): The data dictionary containing train/test/validation data.  

**Returns**:

- `model` (object): The fitted model

### predict

Uses the fitted model to make predictions on data.  

```python
def predict(self, data, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): Data dictionary containing test/train/validation data. 

**Returns**: 

- A data dictionary containing predictions for all classes. 

### predict_df

Makes prediction on a single pandas dataframe. 

```python
def predict_df(self, df) -> Any:
```

**Arguments**: 

- `df` (object): pandas.DataFrame object to use to predict data. 

**Returns**: 

- pandas.DataFrame containing the predictions. 

### predict_proba_df

Makes class predictions on a single pandas dataframe. Only applicable to classification problems. 

```python
def predict_proba_df(self, df) -> Any:
```

**Arguments**: 

- `df` (object): pandas.DataFrame object to use to predict data. 

**Returns**: 

- pandas.DataFrame containing the predictions. 

### get_artifacts

Returns artifacts created during model training. Note that not all frameworks create artifacts, but this is an entry point to access them if they do.  

```python
def get_artifacts(self, id) -> dict[str,Any]:
```

**Arguments**: 

- `id` (str): Experiment id

**Returns**: 

- dictionary containing all relevant artifacts


## Default Methods

The following methods are implemented in the base class. You may find a need to overwrite them as you implement your own model trainers. 

### save

Saves the trained model into `resource_version_control` and logs information into the `metadata_tracker`

```python
def save(self, experiment, *args, **kwargs)
```

**Arguments**: 

- `experiment` (str): The experiment to use to save the model into. 


### _set_model

Setter method for `self.model`. 

```python
def _set_model(self, model):
```

**Arguments**: 

- `model` (object): Model object to assign to `self.model`


### _get_model

Getter method for `self.model`

```python
def _get_model(self) -> Any
```

**Returns**: 

- `self.model`

### calculate_metrics

Calculates performance metrics ont he trained model. 

```python
def calculate_metrics(self, data, predictions, metrics, **kwargs) -> dict[str, float]
```

**Arguments**: 

- `data` (dict): dictonary of train/test/validation data 
- `predictions` (object): 
- `metrics` (list): list of metrics to calculate. Supported metrics include: 
    - `accuracy`
    - `f1` 
    - `rocauc`
    - `prauc`
    - `precision`
    - `recall`
    - `mse`
    - `rmse`
    - `mae`
    - `mape`
    - `mdae`
    - `smape`
    - `r2`
    - `msle`
    - `rmsle`

**Returns**: 

- `metrics_out`: dictionary of computed metrics

### build_model

Simple workflow to build a log a model. This is typically called from withing a `hyperparameter_tuner`, or just on its own if hyperparameter tuning is not used. 

```python
def build_model(self, data, model_version, *args, **kwargs) -> tuple[Any, Any]
```

**Arguments**: 

- `data` (object): dictionary of training/test/valiadation data. 
- `model_version` (object): model version object

**Returns**: 

- `model`: the trained model
- `exp`: experiment where the model was trained

### rebuild_model

Rebuilds a model using all available data 

```python
def rebuild_model(self, data, model_version, *args, **kwargs) -> tuple[Any, Any]
```

**Arguments**: 

- `data` (object): dictionary of training/test/valiadation data. 
- `model_version` (object): model version object

**Returns**: 

- `model`: the trained model
- `exp`: experiment where the model was trained