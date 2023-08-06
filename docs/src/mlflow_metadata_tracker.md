# MLFlowMetadataTracker

The `MLFlowMetadataTracker` class is a Python class that extends the `BaseMetadataTracker` class . It provides methods for logging and retrieving metadata information using MLflow, a popular open-source platform for managing the end-to-end machine learning lifecycle.

In the `MLFlowMetadataTracker` as "resource" is uniquely defined by its `id` and the MLFlow `run` that it is associated with. 

## Attributes

The `MLFlowMetadataTracker` class  sets the following attributes in `__init__` and these should generally be considered available when working with the class: 

- `client` : The `mlflow` client. 
- `run` : The current `mlflow` run. 
- `url` : The `mlflow` tracking url. 

## Configuration

### Required Configuration

The `MLFlowMetadataTracker` class requires the following configuration parameters to be set:

- `mlflow_tracking_uri` (str): The URI of the MLflow tracking server.
- `mlflow_experiment_name` (str): The name of the MLflow experiment to log the metadata.

### Optional Configuration

The `MLFlowMetadataTracker` class has no optional configuration. 

### Default Configuration 

The `MLFlowMetadataTracker` class has no default configuration. 

## Methods

### log_artifact
The `log_artifact` method saves the artifact located at the specified `path` to the artifact directory in the MLflow run associated with the given `resource`. The `id` parameter is used to organize artifacts within the artifact directory.
```python
def log_artifact(self, resource, id, path, *args, **kwargs):
```


**Arguments**:

- `resource` (str, run): A tuple containing the resource id and the MLflow run object.
- `id` (str): A string representing the artifact ID.
- `path` (str): The path to the artifact that needs to be saved.

**Returns**:

- None


### get_artifact
The `get_artifact` method retrieves the artifact with the specified `id` from the MLflow run associated with the given `resource`.

```python
def get_artifact(self, resource, id, *args, **kwargs):

```

**Arguments**:

- `resource` (str, run): A tuple containing the resource id and the MLflow run object.
- `id` (str): A string representing the artifact ID.

**Returns**:

- None


### log_tag
The `log_tag` method sets the tag with the specified `key` and `value` for the MLflow run associated with the given `resource`.

```python
def log_tag(self, resource, key, value, *args, **kwargs):

```

**Arguments**:

- `resource` (str, run): A tuple containing the resource id and the MLflow run object.
- `key` (str): The tag key.
- `value` (str): The tag value.

**Returns**:

- None



### get_tag
The `get_tag` method returns the value of the tag with the specified `key` for the MLflow run associated with the given `resource`.

```python
def get_tag(self, resource, key, *args, **kwargs):

```

**Arguments**:

- `resource` (str, run): A tuple containing the resource id and the MLflow run object.
- `key` (str): The tag key.

**Returns**:

- str: The value of the tag with the specified `key` for the MLflow run associated with the given `resource`.



### log_metadata
The `log_metadata` method saves the metadata with the specified `id` and `data` to the MLflow run associated with the given `resource`. If the `id` contains "param," the data will be saved as both a parameter and a tag for retrieval purposes.

```python
def log_metadata(self, resource, id, data, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): A tuple containing the resource id and the MLflow run object.
- `id` (str): A string representing the metadata ID.
- `data` (any): The metadata to store.

**Returns**:

- None



### get_metadata
The `get_metadata` method returns the value of the metadata with the specified `id` for the MLflow run associated with the given `resource`.

```python
def get_metadata(self, resource, id, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): A tuple containing the resource id and the MLflow run object.
- `id` (str): A string representing the metadata ID.

**Returns**:

- any: The value of the metadata with the specified `id` for the MLflow run associated with the given `resource`.



### create_resource
The `create_resource` method creates a new MLflow run or nested run based on the provided `id`, `type`, and `parent` information. If `type` is "experiment," a nested run will be created under the specified parent resource.

```python
def create_resource(self, id, type=None, parent=None, *args, **kwargs):

```

**Arguments**:

- `id` (str): A string ID of the resource.
- `type` (str, optional): A string with the value "experiment" or None.
- `parent` (str, run, optional): A tuple containing the parent resource id and MLflow run or None.

**Returns**:

- tuple: A tuple containing the new resource ID and the MLflow run.



### get_resource
The `get_resource` method retrieves the resource with the specified `id` and `type` along with its associated MLflow run.

```python
def get_resource(self, id, type, parent=None, *args, **kwargs):


```

**Arguments**:

- `id` (str): A string ID of the resource to retrieve.
- `type` (str): A string with the value "experiment" or None.
- `parent` (str, run, optional): A tuple containing the parent resource id and MLflow run or None.

**Returns**:

- tuple: A tuple containing the resource ID and the MLflow run.


### update_resource
The `update_resource` method updates the resource with the provided `updates` for the MLflow run associated with the given `resource`.

```python
def update_resource(self, resource, updates, *args, **kwargs):
```

**Arguments**:

- `resource` (str, run): A tuple containing the resource id and the MLflow run object.
- `updates` (dict): A dictionary containing the updated information.

**Returns**:

- None


### clean_resource
The `clean_resource` method ends the MLflow run described in the `resource`.

```python
def clean_resource(self, resource, type, *args, **kwargs):

```

**Arguments**:

- `resource` (str, run): A tuple containing the resource id and the MLflow run object.
- `type` (str): A string "experiment" or None.

**Returns**:

- None


### get_prev_resource_version
The `get_prev_resource_version` method returns the previous resource version for the specified `resource` and any additional filters. The `num` parameter controls the number of records to return .

```python
def get_prev_resource_version(self, resource, extra_filters=[], num=1, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): A tuple containing the resource ID and the MLflow run object.
- `extra_filters` (list, optional): A list of extra filters to be applied as strings.
- `num` (int, optional): The number of records to return .

**Returns**:

- tuple: A tuple containing the resource ID and the MLflow run of the previous resource version.


### get_currently_deployed_model_version

The `get_currently_deployed_model_version` method returns the deployed version of the provided model version, if any.

```python
def get_currently_deployed_model_version(self, model_version, *args, **kwargs):


```

**Arguments**:

- `model_version` (str, run): A tuple containing the model version ID and the MLflow run object.

**Returns**:

- tuple: A tuple containing the ID and the MLflow run object of the deployed model version.


### get_prediction_job_model_version

The `get_prediction_job_model_version` method returns the model version ID and the MLflow run object associated with the given prediction job identifier.

```python
def get_prediction_job_model_version(self, prediction_job, *args, **kwargs):


```

**Arguments**:

- `prediction_job` (str, run): A tuple containing the prediction job ID and the MLflow run object or a string representing a prediction job.

**Returns**:

- tuple: A tuple containing the model version ID and the MLflow run object.

### get_latest_model_resource
The `get_latest_model_resource` method returns the latest model version when the type is "prediction_job."


```python
def get_latest_model_resource(self, model, type, *args, **kwargs):


```

**Arguments**:

- `model` (str, run): A tuple containing the model ID and the MLflow run object.
- `type` (str): A string "prediction_job" or other.

**Returns**:

- `model_version` (str, run): tuple containing the model version ID and run.


### get_winning_experiment
The `get_winning_experiment` method returns the ID and the MLflow run object of the experiment that produced the winning model for the provided model version.

```python
def get_winning_experiment(self, model_version, *args, **kwargs):


```

**Arguments**:

- `model_version` (str, run): A tuple containing the model version ID and the MLflow run object.

**Returns**:

- tuple: A tuple containing the ID and the MLflow run object of the experiment that produced the winning model for the provided model version.



### build_model_lineage
The `build_model_lineage` method logs dataset versions used to create the provided model version. It saves the dataset versions in the metadata tags of the model version.

```python
def build_model_lineage(self, model_version, dataset_versions, *args, **kwargs):


```

**Arguments**:

- `model_version` (str, run): The model version object.
- `dataset_versions` (list[str, run]): A list of dataset version objects.

**Returns**:

- None



### get_resource_id
The `get_resource_id` method returns the ID of the given resource. It can extract the ID from the resource or modify it according to specific rules.

```python
def get_resource_id(self, resource, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): The resource object.

**Returns**:

- str: The ID of the given resource.



### get_parent_id
The `get_parent_id` method returns the parent ID of a resource, currently only applicable for experiments.

```python
def get_parent_id(self, resource, type=None, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): The resource object.
- `type` (str, optional): The resource type.

**Returns**:

- str: parent_id: str, or None



### register_vc_resource
The `register_vc_resource` method registers information received from a version control component into the metadata tracker. It saves information related to the version control system, such as commit information, to the specified `resource`.

```python
def register_vc_resource(self, resource, vc_info, key=None, additional_metadata={}, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): The resource to log `vc_info` into.
- `vc_info` (dict): A dictionary of information returned by the version control component.
- `key` (str, optional): The key to append to values to be logged.
- `additional_metadata` (dict, optional): Additional metadata to log.

**Returns**:

- None



### get_vc_info
The `get_vc_info` method returns the resource version control information that was previously logged. It retrieves version control information, such as commit details, associated with the specified `resource`.

```python
def get_vc_info(self, resource, key="hexsha", *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): The resource to fetch `vc_info` from .
- `key` (str, optional): The key used when saving `vc_info`.

**Returns**:

- dict: Returns the information needed to retrieve an object from the version control system. This typically includes details like a git hexsha.



### log_data_profile
The `log_data_profile` method logs a data profile to the specified `resource`. It saves the data profile as an artifact in the MLflow run associated with the given `resource`.

```python
def log_data_profile(self, resource, file_path, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): The resource to log the data profile into.
- `file_path` (str): The file path of the data profile.

**Returns**:

- None



### get_data_profile
The `get_data_profile` method retrieves the data profile with the specified `id` from the MLflow run associated with the given `resource`.

```python
def get_data_profile(self, resource, id, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): The resource to fetch the data profile from .
- `id` (str): A string representing the data profile ID.

**Returns**:

- None



### log_checks
The `log_checks` method logs a data check into the specified `resource`. It saves the data check report as an artifact in the MLflow run associated with the given `resource`.

```python
def log_checks(self, resource, file_path, type="data", *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): The resource to log the data check into.
- `file_path` (str): The file path of the data check.
- `type` (str, optional): The type of check. Defaults to "data".

**Returns**:

- None



### get_data_checks
The `get_data_checks` method retrieves the data checks with the specified `id` from the MLflow run associated with the given `resource`.

```python
def get_data_checks(self, resource, id, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): The resource to fetch the data checks from .
- `id` (str): A string representing the data checks ID.

**Returns**:

- None



### log_data_comparison
The `log_data_comparison` method logs a data comparison into the specified `resource`. It saves the data comparison result as an artifact in the MLflow run associated with the given `resource`.

```python
def log_data_comparison(self, resource, file_path, *args, **kwargs):


```

**Arguments**:

- `resource` (str, run): The resource to log the data comparison into.
- `file_path` (str): The file path of the data comparison.

**Returns**:

- None



### stop

The `stop` method stops any currently active MLflow runs associated with the metadata tracker.

```python
def stop(self, *args, **kwargs):


```


### load_model
The `load_model` method loads a model trainer object from the metadata tracker.

```python
def load_model(self, model_obj, model_version, ref_model, pipeline_config={}, *args, **kwargs):
```

**Arguments**:

- `model_obj` (object): A fitted model 
- `model_version` (str, run): The model version to use to retrieve the model trainer
- `ref_model` (object): A model trainer object to use as a reference. I.E. will have similar configs, etc
- `pipeline_config` (dict, optional): pipeline config to pass. Defaults to {}.

**Returns**:

- `model`: the model trainer object



## Example Usage

```python
from lolpop.components import MLFlowMetadataTracker 

config = {
    #insert component config here
}

# Create an instance of MLFlowMetadataTracker
metadata_tracker = MLFlowMetadataTracker(conf=config)

#log artifact
resource = metadata_tracker.create_resource("my_model", type="model")
metadata_tracker.log_artifact(resource, "my_artifact", "path/to/my_model.pkl")

# Retrieve artifacts
artifact = metadata_tracker.get_artifact(resource, "my_artifact")
```

