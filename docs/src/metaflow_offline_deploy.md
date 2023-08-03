### MetaflowOfflineDeploy

The `MetaflowOfflineDeploy` class is a subclass of `BaseDeploy` and provides methods for running a Metaflow flow object and obtaining artifacts from the `MetaflowOfflineDeploy` pipeline.


## Attributes

- `METAFLOW_CLASS` - The name of the class that inherits from metaflow's `FlowSpec`

## Configuration 

### Required Configuration 

`MetaflowOfflineDeploy` requires the following component types: 

- `metadata_tracker`
- `model_repository`
- `model_deployer`
- `resource_version_control`


## Methods

### run
This method runs the MetaflowOfflineDeploy. It loads a Metaflow flow object based on the current file, loads the flow, and then runs it using the model and version provided. This method logs execution and does not return any value.

```python
def run(self, model, model_version, *args, **kwargs):
```

**Parameters**:

- `model` (object): The model object.
- `model_version` (object): The model version object.


### get_artifacts

This method obtains artifacts of the MetaflowOfflineDeploy. It gets the latest run of the MetaflowOfflineDeploy pipeline and returns the requested artifacts.

```python
def get_artifacts(self, artifact_keys):
```

**Parameters**:

- `artifact_keys` (list): A list of keys for the artifacts being requested.

**Returns**:
- `artifacts` (dict): A dictionary of requested artifacts.

## MetaflowOfflineDeploySpec Methods

`MetaflowOfflineDeploySpec` contains the following methods. These are mirrored from the `OfflineDeploy` class, and you should see that documentation for more information (Note: instead of these method explicitly using arguments, they instead access saved artifacts during the Metaflow run). 

- `start`
- `promote_model`
- `approve_model`
- `deploy_model`
- `check_approval`
- `end`