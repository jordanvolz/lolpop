## Overview

A `model_visualizer` is a component that produces visualizations for a model on a given dataset. The visualiztions will be highly dependent upon the problem type, but these are things like confusion matrices, ROCAUC curves, and forecast plots.  


## Attributes

`BaseModelVisualizer` contains no default attributes. 

## Configuration

`BaseModelVisualizer` contains no default or required configuration. 


## Interface

The following methods are part of `BaseModelVisualizer` and should be implemented in any class that inherits from this base class: 

### generate_viz

Generates visualizations for the given model on the provided data.  

```python
def generate_viz(self, data, model, *args, **kwargs)
```

**Arguments**: 

- `data` (object): The data dictionary containing train/test/validation data.  
- `model` (object): The fitted model

