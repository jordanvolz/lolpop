## Overview

A `data_checker` is a component that takes a dataset and runs some data checks on that data. These data checks are typically concerned with things like data quality and data integrity. 

## Attributes

`BaseLogger` contains the following default attributes: 

- `url` : The url of the log, if applicable. 

## Configuration

`BaseLogger` contains no default or required configuration. 


## Interface

The following methods are part of `BaseLogger` and should be implemented in any class that inherits from this base class: 

### log

Logs a message to the specified log level. 

```python
def log(self, msg, level)
```

**Arguments**: 

- `msg` (str): The message to log. 
- `level` (str): The log level to use. I.E. "ERROR", "WARN", "INFO", etc. 