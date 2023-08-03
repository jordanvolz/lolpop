# MetaflowOfflineTrain

The `MetaflowOfflineTrain` class is a subclass of `BaseTrain` and provides methods for running a Metaflow pipeline and retrieving artifacts associated with the pipeline run.

## Attributes

- `METAFLOW_CLASS` - The name of the class that inherits from metaflow's `FlowSpec`

## Configuration 

### Required Configuration 

The `MetaflowOfflineTrain` requires the following components: 

- `data_splitter`
- `metadata_tracker`
- `resource_version_control`
- `model_explainer`
- `model_checker`
- `model_visualizer`
- `model_bias_checker` 

## Methods

### run 
The `run()` method executes the Metaflow pipeline with the provided data. It takes a pandas dataframe `data` as input, which represents the data to be used in the training process. 

```python
def run(self, data, *args, **kwargs)
```
**Arguments**:

- `data` (dict): The dictionary of train/test/validation data, returned by the data_splitter component. 

**Returns**

None

### get_artifacts
he `get_artifacts()` method retrieves the artifacts associated with the Metaflow pipeline run. It takes a list of artifact keys `artifact_keys` as input, representing the artifacts to retrieve from the run. The method returns a dictionary `artifacts` containing the retrieved artifacts.

```python
def get_artifacts(self, artifact_keys):
```
 
**Arguments**:

- `artifact_keys` (list): A list of artifact keys to retrieve.

**Returns**

- `artifacts` (dict): A dictionary containing the requested artifacts.


## MetaflowOfflineTrainSpec Methods

`MetaflowOfflineTrainSpec` contains the following methods. These are mirrored from the `OfflineTrain` class, and you should see that documentation for more information (Note: instead of these method explicitly using arguments, they instead access saved artifacts during the Metaflow run). 

- `start`
- `split_data`
- `train_model`
- `check_model`
- `analyze_model`
- `compare_models`
- `check_model_bias`
- `retrain_model_on_all_data`
- `end`