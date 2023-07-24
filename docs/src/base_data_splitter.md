## Overview

A `data_splitter` is a component that takes a dataset and splits it into training, validation, and test datasets. This is intended to properly split data for use in machine learning workflows, dependent upon the `problem_type` of the workflow. 


## Attributes

`BaseDataSplitter` contains no default attributes. 

## Configuration

`BaseDataSplitter` contains no default or required configuration. 


## Interface

The following methods are part of `BaseDataSplitter` and should be implemented in any class that inherits from this base class: 

### spit_data

Performs a data split on the given data. 

```python
def split_data(self, data, *args, **kwargs) -> dict[str, Any]
```

**Arguments**: 

- `data` (object): The data to split.  

**Returns**:

- `data_out` (dict): A dictionary containing the split datasets (train, validation, test)

### get_train_test_dfs

Performs a data comparison between two data profiles.

```python
def get_train_test_dfs(self, data,*args, **kwargs) -> tuple[Any, Any]
```

**Arguments**: 

- `data` (dict): The dictionary of split datasets 

**Returns**:

- `data_out` (tuple): A (`train`, `test`) tuple containing the combined training and test datasets. 