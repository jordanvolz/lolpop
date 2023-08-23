## Overview

A `metadata_tracker` is a component that logs artifacts and metadata relative to a machine learning workflow *run*. A run can be viewed as a collection of actions that defines a full workflow, such as training a model, making predictions, etc. A `metadata_tracker` is expected to have an internal concept of run which users can leverage, and log necessary information for tracking purposes into that run.  

The `BaseMetadataTracker` class attempts to provide a consistent interface that can be implemented by any specific type of metadata tracker. 

## Attributes

`BaseMetadataTracker` contains the following default attributes: 

- `url`: The url of the metadata tracker. 

## Configuration

### Required Configuration 

`BaseMetadataTracker` has no required configuration.

## Interface

The following methods are part of `BaseMetadataTracker` and should be implemented in any class that inherits from this base class: 

### log_artifact
Logs an artifact into a resource in the metadata tracker. 

```python
def log_artifact(self, resource, id, path, *args, **kwargs):
```

**Arguments**:

- `resource` (object): The resource in the metadata tracker to log the artifact to. 
- `id` (str): A string representing the artifact ID.
- `path` (str): The path to the artifact that needs to be saved.

**Returns**:

- None


### get_artifact
Retrieves an artifact from the metadata tracker. 

```python
def get_artifact(self, resource, id, *args, **kwargs) -> Any:

```

**Arguments**:

- `resource` (object): The resource in the metadata tracker
- `id` (str): A string representing the artifact ID.

**Returns**:

- None


### log_tag
Logs a key-value tag to the metadata tracker resource. 

```python
def log_tag(self, resource, key, value, *args, **kwargs):

```

**Arguments**:

- `resource` (object): The resource in the metadata tracker to log the tag into. 
- `key` (str): The tag key.
- `value` (str): The tag value.

**Returns**:

- None



### get_tag
Retrieves a tage value from the metadata tracker. 

```python
def get_tag(self, resource, key, *args, **kwargs) -> Any:

```

**Arguments**:

- `resource` (object): The metadata tracker resource. 
- `key` (str): The tag key.

**Returns**:

- Any: The value of the tag with the specified `key` for the MLflow run associated with the given `resource`.



### log_metadata
Logs metadata into the metadata tracker resource. 

```python
def log_metadata(self, resource, id, data, *args, **kwargs):


```

**Arguments**:

- `resource` (object): The metadata tracker resource. 
- `id` (str): A string representing the metadata ID.
- `data` (any): The metadata to store.

**Returns**:

- None



### get_metadata
Retrieves metadata from the metadata tracker resource. 

```python
def get_metadata(self, resource, id, *args, **kwargs) -> Any:


```

**Arguments**:

- `resource` (object): The metadata tracker resource. 
- `id` (str): A string representing the metadata ID.

**Returns**:

- any: The value of the metadata with the specified `id` for the MLflow run associated with the given `resource`.



### create_resource
Creates a new resource in the metadata tracker. 

```python
def create_resource(self, id, type=None, *args, **kwargs) -> Any:

```

**Arguments**:

- `id` (str): A string ID of the resource.
- `type` (str, optional): A string with the value "experiment" or None.

**Returns**:

- object: An object from the metadata tracker representing the resource. 



### get_resource
Retrieves a resource from the metadata tracker. 

```python
def get_resource(self, id, type, *args, **kwargs) -> Any:


```

**Arguments**:

- `id` (str): A string ID of the resource to retrieve.
- `type` (str): A string with the value "experiment" or None.

**Returns**:

- object: The resource from the metadata_tracker


### update_resource
Updates a resource in the metadata tracker.

```python
def update_resource(self, resource, updates, *args, **kwargs) -> Any:
```

**Arguments**:

- `resource` (object): A tuple containing the resource id and the MLflow run object.
- `updates` (dict): A dictionary containing the updated information.

**Returns**:

- The updated resource.


### clean_resource
Cleans up a resource. The main use is by experiments to ensure that any resources craeted by the experiment have been properly delt with. 

```python
def clean_resource(self, resource, type, *args, **kwargs):

```

**Arguments**:

- `resource` (object): The resource to clean. 
- `type` (str): The type of resource. 

**Returns**:

- None


### get_prev_resource_version
Returns the previous version of a resource. 

```python
def get_prev_resource_version(self, resource, *args, **kwargs) -> Any:


```

**Arguments**:

- `resource` (object): A resource version. 


**Returns**:

- object: The previous version of the resource. 


### get_currently_deployed_model_version

Returns the currently deployed model version. 

```python
def get_currently_deployed_model_version(self, model_version, *args, **kwargs) -> Any:


```

**Arguments**:

- `model_version` (object): The model version resource. 

**Returns**:

- object: The currently deployed model version


### get_prediction_job_model_version

Returns the model version used in a prediction job.

```python
def get_prediction_job_model_version(self, prediction_job, *args, **kwargs) -> Any:


```

**Arguments**:

- `prediction_job` (object): The prediction job resource. 

**Returns**:

- object: The model version resouce. 

### get_latest_model_resource
Returns the latest resource from a model resource. Most commonly probably used to return the latest prediction job created from a model resource. 


```python
def get_latest_model_resource(self, model, type, *args, **kwargs) -> Any:


```

**Arguments**:

- `model` (object): The model resource. 
- `type` (str): The type of resource to return the latest version of. 

**Returns**:

-  (object): The latest version of the `type` specified. 


### get_winning_experiment
Returns the winning experiment from a model version. 

```python
def get_winning_experiment(self, model_version, *args, **kwargs) -> Any:


```

**Arguments**:

- `model_version` (object): The model version object. 

**Returns**:

- object: The winning experiment. 



### build_model_lineage
Logs dataset versions used to create the provided model version.

```python
def build_model_lineage(self, model_version, dataset_versions, *args, **kwargs):


```

**Arguments**:

- `model_version` (object): The model version object.
- `dataset_versions` (list[object]): A list of dataset version objects.

**Returns**:

- None



### get_resource_id
Returns the id of the resource.

```python
def get_resource_id(self, resource, *args, **kwargs) -> str:


```

**Arguments**:

- `resource` (object): The resource object.

**Returns**:

- str: The ID of the given resource.



### get_parent_id
Returns the id of the parent resource, if any. 

```python
def get_parent_id(self, resource, type=None, *args, **kwargs) -> str:


```

**Arguments**:

- `resource` (object): The resource object.
- `type` (str, optional): The resource type.

**Returns**:

- str: parent_id: str, or None



### register_vc_resource
The `register_vc_resource` method registers information received from a version control component into the metadata tracker. It saves information related to the version control system, such as commit information, to the specified `resource`.

```python
def register_vc_resource(self, resource, vc_info, key=None, additional_metadata={}, *args, **kwargs):


```

**Arguments**:

- `resource` (object): The resource to log `vc_info` into.
- `vc_info` (dict): A dictionary of information returned by the version control component.
- `key` (str, optional): The key to append to values to be logged.
- `additional_metadata` (dict, optional): Additional metadata to log.

**Returns**:

- None



### get_vc_info
The `get_vc_info` method returns the resource version control information that was previously logged. It retrieves version control information, such as commit details, associated with the specified `resource`.

```python
def get_vc_info(self, resource, key="hexsha", *args, **kwargs) -> dict[str, Any]:


```

**Arguments**:

- `resource` (object): The resource to fetch `vc_info` from .
- `key` (str, optional): The key used when saving `vc_info`.

**Returns**:

- dict: Returns the information needed to retrieve an object from the version control system. This typically includes details like a git hexsha.



### log_data_profile
The `log_data_profile` method logs a data profile to the specified `resource`.

```python
def log_data_profile(self, resource, file_path, *args, **kwargs):


```

**Arguments**:

- `resource` (object): The resource to log the data profile into.
- `file_path` (str): The file path of the data profile.

**Returns**:

- None


### log_checks
The `log_checks` method logs a data check into the specified `resource`.

```python
def log_checks(self, resource, file_path, *args, **kwargs):


```

**Arguments**:

- `resource` (object): The resource to log the data check into.
- `file_path` (str): The file path of the data check.

**Returns**:

- None




### log_data_comparison
The `log_data_comparison` method logs a data comparison into the specified `resource`. 

```python
def log_data_comparison(self, resource, file_path, *args, **kwargs):


```

**Arguments**:

- `resource` (object): The resource to log the data comparison into.
- `file_path` (str): The file path of the data comparison.

**Returns**:

- None



### stop

The `stop` method stops the active run. 

```python
def stop(self, *args, **kwargs):


```

### load_model
The `load_model` method loads a model trainer object from the metadata tracker.

```python
def load_model(self, model_obj, model_version, ref_model, pipeline_config={}, *args, **kwargs) -> Any:
```

**Arguments**:

- `model_obj` (object): A fitted model 
- `model_version` (str, run): The model version to use to retrieve the model trainer
- `ref_model` (object): A model trainer object to use as a reference. I.E. will have similar configs, etc
- `pipeline_config` (dict, optional): pipeline config to pass. Defaults to {}.

**Returns**:

- `model`: the model trainer object