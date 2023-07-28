## Overview

A `model_repository` is a component that tracks model version promotions and approvals. It acts as a bridge between development systems (i.e. model training) and production systems (i.e. inference).  


## Attributes

`BaseModelRepository` contains no default attributes. 

## Configuration

`BaseModelRepository` contains no required components or configuration.  

## Interface

The following methods are part of `BaseModelRepository` and should be implemented in any class that inherits from this base class: 

### register_model

Registers a model version with the model repository. 

```python
 def register_model(self, model_version, model, *args, **kwargs) -> Any
```

**Arguments**: 

- `model_version` (object): The model version to register.  
- `model` (object): The model being registered.

**Returns**:

- `str`: id of the registered model version in the model repository. 

### promote_model

Promotes a registered model. 

```python
def promote_model (self, id, *args, **kwargs)
```

**Arguments**: 

- `id` (str): ID of the registered model to promote.  

### approve_model

Marks a promoted model version as approved.

```python
def promote_model (self, id, *args, **kwargs)
```

**Arguments**: 

- `id` (str): ID of the promoted model to approve.  

### check_approval

Checks if a registered or promoted model has been approved.

```python
def check_approval (self, id, *args, **kwargs) -> bool
```

**Arguments**: 

- `id` (str): ID of the registered model to chec. 

**Returns**: 

- `bool`: Whether the registered model is approved. 