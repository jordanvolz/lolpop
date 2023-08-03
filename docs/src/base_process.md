## Overview

The `process` pipeline is a pipeline that performs common data processing activities, such as making data transformations, versioning data, performing data checks and data drift analysis, etc. 

## Attributes

`BaseProcess` contains the following attributes: 

- `datasets_used` (list): A list of datasets used in the workflow. The intention here is to gather relevant datasets used in model construction for purposes of generating lineage downstream. 

## Configuration

`BaseProcess` contains no default or required configuration. 


## Interface

The following methods are part of `BaseProcess` and should be implemented in any class that inherits from this base class: 

### transform_data

Executes a data transformation

```python
def transform_data(self, source, *args, **kwargs) -> Any
```

**Arguments**: 

- `source` (str): The source identifier of the input data (or possibly transform job). This should be something like a file path or a table name, etc. 


**Returns**:

- `data` (object): The transformed data


### track_data

Versions a dataset. 

```python
def track_data(self, data, id, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): The dataset to version.
- `id` (object): The dataset id. 

**Returns**:

- `dataset_version` (object): The dataset_version corresponding to the versioned data. 


### profile_data

Creates an EDA-style data profile.

```python
def profile_data(self, data, dataset_version, *args, **kwargs)
```

**Arguments**: 

- `data` (object): The data to profile.
- `dataset_version` (object): The dataset version to save the profile in. 

**Returns**:

Nothing 

### check data

Runs data checks on the dataset to detect issues, such as large number of nulls, class imbalance, etc. Checks will vary based on problem type. 

```python
def check_data(self, data, dataset_version, *args, **kwargs)
```

**Arguments**: 

- `data` (object): The data to check.
- `dataset_version` (object): The dataset version to save the data check report in. 

**Returns**:

Nothing

### compare_data

Runs a data drift analysis and generates a drift report. 

```python
def compare_data(self, data, dataset_version, *args, **kwargs)
```

**Arguments**: 

- `data` (object): The data to analyze.
- `dataset_version` (object): The dataset version to save the data drift report in.  

**Returns**:

Nothing
