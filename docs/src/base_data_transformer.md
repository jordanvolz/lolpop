## Overview

A `data_transformer` is a component that transforms data. This is usually done as part of a pre-processing step in a ML workflow. 

## Attributes

`BaseDataConnector` contains no default attributes. 

## Configuration

`BaseDataConnector` contains no default or required configuration. 


## Interface

The following methods are part of `BaseDataConnector` and should be implemented in any class that inherits from this base class: 

### transform

Transforms data. 

```python
def transform(self, source, *args, **kwargs) -> Any
```

**Arguments**: 

- `source` (object): The source data to transform. This could be something like a local python object (pandas.DataFrame), or a SQL query that gets run to generate data in a data warehouse. 

**Returns**:

- `data` (Any): Returns a data object, such as a `pandas` Dataframe.

