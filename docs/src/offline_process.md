# OfflineProcess

The `OfflineProcess` class is a subclass of the `BaseProcess` class and is used for offline data processing. It provides methods for transforming, tracking, profiling, checking, and comparing data.

## Configuration 

### Required Configuration 

The `OfflineProcess` requires the following components: 

- `data_transformer`
- `metadata_tracker`
- `resource_version_control`
- `data_checker`
- `data_profiler` 

## Methods

### transform_data 

Transforms source data by calling the `data_transformer` class method.

```python 
def transform_data(source_data_name, *args, **kwargs)
```

**Arguments:**

- `source_data_name` (str): A string containing the name of the source data.

**Returns:**

- `data_out`: The transformed data.

### track_data 
Tracks the data by creating a dataset version and registering version control metadata.

```python
def track_data(data, id, *args, **kwargs)
```


**Arguments:**

- `data` (object): The data to be tracked.
- `id` (str): The id of the dataset version.

**Returns:**

- `dataset_version`: The dataset version of the registered version control metadata.

### profile_data 
Profiles the data by logging the data profile to the metadata tracker.

```python 
def profile_data(data, dataset_version, *args, **kwargs)
```


**Arguments:**

- `data` (object): The data to be profiled.
- `dataset_version` (object): The dataset version of the registered version control metadata.

**Returns:**

- None

### check_data 
Checks the data by logging a data report to the metadata tracker and sending a notification if `checks_status` is `ERROR` or `WARN`.

```python 
def check_data(data, dataset_version, *args, **kwargs)
```

**Arguments:**

- `data` (object): The data to be checked.
- `dataset_version` (object): The dataset version of the registered version control metadata.

**Returns:**

- None

### compare_data 
Compares a dataset version with the previous version and logs a comparison report to the metadata tracker.

```python 
compare_data(data, dataset_version, *args, **kwargs)
```


**Arguments:**

- `data` (object): The data to be compared.
- `dataset_version` (object): The dataset version of the registered version control metadata.

**Returns:**

- None

