# `MetaflowOfflineProcess` Class

The `MetaflowOfflineProcess` class is a subclass of the `BaseProcess` class and provides functionality to execute the offline Metaflow flow.

## Attributes

- `METAFLOW_CLASS` - The name of the class that inherits from metaflow's `FlowSpec`

## Configuration 

### Required Configuration 

The `MetaflowOfflineProcess` requires the following components: 

- `data_transformer`
- `metadata_tracker`
- `resource_version_control`
- `data_checker`
- `data_profiler` 

## Methods

### run 
Execute the offline Metaflow flow.

```python 
def run(self, source_data_name, source_data, **kwargs)
```

**Arguments**:

- `source_data_name` (str): The name of the data source.
- `source_data` (object): The object containing the source data.

**Returns**

None

### get_artifacts 
Retrieve artifacts from the latest run of the pipeline.

```python 
get_artifacts(self, artifact_keys)
```


**Arguments**:

- `artifact_keys` (list): A list of artifact keys to retrieve.

**Returns**

- `artifacts` (dict): A dictionary containing the requested artifacts.


## MetaflowOfflineProcessSpec Methods

`MetaflowOfflineProcessSpec` contains the following methods. These are mirrored from the `OfflineProcess` class, and you should see that documentation for more information (Note: instead of these method explicitly using arguments, they instead access saved artifacts during the Metaflow run). 

- `start`
- `transform_data`
- `track_data`
- `profile_data`
- `check_data`
- `compare_data`
- `end`