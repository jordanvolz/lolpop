## Overview

A `data_checker` is a component that takes a dataset and runs some data checks on that data. These data checks are typically concerned with things like data quality and data integrity. 

## Attributes

`BaseDataChecker` contains no default attributes. 

## Configuration

`BaseDataChecker` contains no default or required configuration. 


## Interface

The following methods are part of `BaseDataChecker` and should be implemented in any class that inherits from this base class: 

### check_data

Performs a data check on the given data. 

```python
def check_data(self, data, *args, **kwargs) -> tuple[Any, str, str]
```

**Arguments**: 

- `data` (object): The data to check.  

**Returns**:

- `data_report` (Any): Python object of the data report.
- `file_path` (string): Path to the exported report.
- `checks_status` (string): Status of the checks ("PASS"/"WARN"/"ERROR", etc.)