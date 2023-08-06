## Overview

A `model_bias_checker` is a component that takes a ML model and runs some checks on that model. These model checks are typically concerned with things like bias and fairness.  

## Attributes

`BaseModelBiasChecker` contains no default attributes. 


## Configuration

`BaseModelBiasChecker` contains no default or required configuration. 


## Interface

The following methods are part of `BaseModelBiasChecker` and should be implemented in any class that inherits from this base class: 

### check_model_bias

Checks a model for bias. 

```python
def check_model_bias(self, data, model, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (dict): A dictionary contains the data splits.
- `model` (object): The model to check. 

**Returns**: 

- A dictionary of bias metrics and their values.  