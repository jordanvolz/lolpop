## Overview

A `data_connector` is a component that saves and loads data into a data management system (such as an object store or database). 

## Attributes

`BaseDataConnector` contains no default attributes. 

## Configuration

`BaseDataConnector` contains no default or required configuration. 


## Interface

The following methods are part of `BaseDataConnector` and should be implemented in any class that inherits from this base class: 

### get_data

Retrieves data from the data system. 

```python
def get_data(self, source, *args, **kwargs) -> Any
```

**Arguments**: 

- `source` (str): The data to retrieve. This should be something like a table name or a path within the object store, etc.   

**Returns**:

- `data` (Any): Returns a data object, such as a `pandas` Dataframe.


### save_data

Saves the given data to the data system.

```python
def save_data(self, data, target, *args, **kwargs)
```

**Arguments**: 

- `data` (object): The data object to save.

**Returns**: 
Nothing.


### _load_data

Loads data from the data system. This is similar to `get_data` except an explicit configuration is passed in. This enables accessing data with different configurations from the same data_connector component (i.e. different databases within a data warehouse, etc.)

```python
def _load_data(self, source, config, *args, **kwargs) -> Any
```

**Arguments**: 

- `source` (str): The data to retrieve. This should be something like a table name or a path within the object store, etc.   

**Returns**:

- `data` (Any): Returns a data object, such as a `pandas` Dataframe.

### _save_data

Saves data to the data system. This is similar to `save_data` except an explicit configuration is passed in. This enables saving data with different configurations with the same data_connector component (i.e. different databases within a data warehouse, etc.)

```python
 def _save_data(self, data, config, *args, **kwargs)
 ```
**Arguments**: 

- `data` (object): The data object to save.

**Returns**: 
Nothing.

