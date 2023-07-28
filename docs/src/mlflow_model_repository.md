# MLFlowModelRepository

## Description
The `MLFlowModelRepository` class is a custom repository implementation specifically designed to work with MLFlow models. It extends the `BaseModelRepository` class and provides methods for registering and promoting MLFlow models. This class also interacts with a metadata tracker to log and manage the status of models.

## Configuration 

### Required Configuration 

 `MLFlowModelRepository` also requires the following components: 

 - `metadata_tracker`: Only the `MlFlowMetadataTracker` is supported.  

### Optional Configuration 

`MLFlowModelRepository` also requires the following components: 

- `mlflow_tracking_uri`: The URI of the MLFlow instance. This is only used if no `metadata_tracker` component is passed in during initialization.
- `mlflow_experiment_name`: The MLFlow experiment name to use. This is only used if no `metadata_tracker` component is passed in during initialization. 

### Default Configuration 

`MLFlowModelRepository` has no default configuration. 

## Methods

### `__init__` 
This method initializes the `MLFlowModelRepository` class. It sets up the configuration and connections to MLFlow based on the provided components. If a metadata tracker is used for metadata tracking, the connection details are obtained from the tracker. Otherwise, the MLFlow tracking URI and experiment name are retrieved from the configuration. This method also logs the MLFlow configuration details.

```python 
def __init__(self, components={}, *args, **kwargs)
```


**Arguments**

- `components` (dict): A dictionary containing the components used by the repository. Default is an empty dictionary.
- `*args`: Additional positional arguments.
- `**kwargs`: Additional keyword arguments.

### register_model 
This method registers a model in MLFlow and returns the name of the registered model. The method uses the MLFlow module specified in the model object to log the model. If the model is already registered, this method will simply bump up the version number.

```python 
register_model(self, model_version, model, *args, **kwargs)
```

**Arguments**

- `model_version` (object): The version of the model to register.
- `model` (object): The model object associated with the model_version. I.E. the winning experiment's model object.

**Returns**

- `reg_name` (str): The name of the registered model.

### promote_model 
This method promotes the specified registered model to a given stage and logs the promotion in the metadata tracker. The method transitions the model version from the starting stage to the target stage in MLFlow. It also allows the demotion of previous instances of the registered model if required.

``` python
def promote_model(self, registered_model_name, from_stage="None", to_stage="Production", demote_previous_model_versions=True, *args, **kwargs)
```

**Arguments**

- `registered_model_name` (str): The name of the registered model to promote.
- `from_stage` (str): The starting stage of the registered model. Default is "None".
- `to_stage` (str): The target stage to promote the registered model to. Default is "Production".
- `demote_previous_model_versions` (bool): A boolean variable to enable or disable demotion of previous instances of the registered model. Default is True.

**Returns**

- `model_version` (tuple): A tuple containing the ID of the registered model and an MLFlow run object for the promoted model version.

### check_approval 
This method checks the approval status of a promotion. Currently, approvals are not implemented in MLFlow, so this method always returns True.

```python 
def check_approval(self, promotion, *args, **kwargs)
```

**Arguments**

- `promotion` (object): The promotion object.

**Returns**

- `True` (bool): Always returns True.

### approve_model 
This method approves a promotion. Currently, approvals are not implemented in MLFlow, so this doesn't do anything.

```python 
def approve_model(self, promotion, *args, **kwargs)
```

**Arguments**

- `promotion` (object): The promotion object.


## Example Usage
```python
# Import the necessary modules
from lopop.component import MLFlowModelRepository

... #create model and model_versions

config = {
    #insert component config here 
}

# Create an instance of the MLFlowModelRepository class
repo = MLFlowModelRepository(conf=config)

# Register a model
reg_name = repo.register_model(model_version, model)

# Promote the registered model
from_stage = "None"
to_stage = "Test"
model_version = repo.promote_model(reg_name, from_stage, to_stage)
```