## Overview

A `data_profiler` is a component that takes a dataset and runs some analysis on that data. This is intended to provide the ability to profile data or provide [EDA](https://en.wikipedia.org/wiki/Exploratory_data_analysis) capabilities in a workflow.

A `data_profiler` should also be able to compare different data reports to understand if two snapshots of a dataset have significantly changed. This can be used for data drift calculations. 

## Attributes

`BaseDataProfiler` contains no default attributes. 

## Configuration

`BaseDataProfiler` contains no default or required configuration. 


## Interface

The following methods are part of `BaseDataProfiler` and should be implemented in any class that inherits from this base class: 

### profile_data

Performs a data check on the given data. 

```python
def profile_data(self, data, *args, **kwargs) -> tuple[Any, str]
```

**Arguments**: 

- `data` (object): The data to profile.  

**Returns**:

- `data_profile` (Any): Python object of the data profile.
- `file_path` (string): Path to the exported report.

### compare_data

Performs a data comparison between two data profiles.

```python
def compare_data(self, data, prev_data, *args, **kwargs) -> tuple[Any, str]
```

**Arguments**: 

- `data` (object): The current data profile.  
- `prev_data` (object): A previous data profile.  

**Returns**:

- `data_profile` (Any): Python object of the data profile.
- `file_path` (string): Path to the exported report.