## Overview

A `model_explainer` is a component that takes is focused on model interpretability. It should be able to generated things like feature importance for models and explanations for predictions from a model.  

## Attributes

`BaseModelExplainer` contains no default attributes. 

## Configuration

`BaseModelExplainer` contains no required components. 


## Interface

The following methods are part of `BaseModelExplainer` and should be implemented in any class that inherits from this base class: 

### get_feature_importance

Generates feature importance for a given model. 

```python
def get_feature_importance(self, data, model, *args, **kwargs) -> tuple(Any, Any)
```

**Arguments**: 

- `data` (dict): A dictionary of train/test data.  
- `model` (object): The model to use.

**Returns**:

- `explanations_train` (Any): Explanations for the training dataset
- `explanations_test` (Any): Explanations for the test dataset

### get_explanations

Generates individual explanations for each row of the given dataset. 

```python
def get_explanations(self, data, model, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): The data to generate explanations for. Likely a pandas.DataFrame.
- `model` (object): The model to use. 

**Returns**:

- `explanations` (Any): Explanations for the model on the given data. 