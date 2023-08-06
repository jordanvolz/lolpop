## Overview

A `metrics_tracker` is a component that logs metrics relative to a machine learning workflow over time. Metrics tracking may be tightly related to metadata tracking, or an entirely different component. To allow for flexibility of implementation, the design of the base class is such that a standalone component should be able to be utilized, even though many may opt to leverage a more tightly integrated solution.


## Attributes

`BaseMetricsTracker` contains the following default attributes: 

- `url`: The url of the metrics tracker. 

## Configuration

### Required Configuration 

`BaseMetricsTracker` has no required configuration.

## Interface 


### log_metric
Logs a metric with the corresponding resource ID, metric ID, and metric value.

```python 
def log_metric(self, resource, id, value, *args, **kwargs)
```

**Arguments**: 

- `resource` (object): A resource object.
- `id` (str): A unique identifier for the metric.
- `value` (Any): The value of the metric.


### get_metric
Retrieves a metric with the corresponding resource ID and metric ID.

```python 
def get_metric(self, resource, id, *args, **kwargs)
```

- `resource` (object): A resource object.
- `id` (str): The metric ID.

**Returns**: 

- The metric value. 

### log_metrics 
Logs multiple metrics with the corresponding resource ID.

```python 
def log_metrics(self, resource, metrics, *args, **kwargs)
```


**Arguments**: 

- `resource` (object): A resource object.
- `metrics` (dict): A dictionary containing the metrics to log. 

### copy_metrics 
Copies metrics from one resource to another.

```python
de copy_metrics(self, from_resource, to_resource, *args, **kwargs)
```

**Arguments**: 

- `from_resource` (object): The resource to copy metrics from.
- `to_resource` (object): The resource to copy metrics to.

### log_prediction_metrics 
Logs prediction metrics with the corresponding prediction job ID and list of predictions.

```python
def log_prediction_metrics(self, prediction_job, predictions, *args, **kwargs)
```

**Arguments**: 

- `prediction_job` (object): A prediction job object.
- `predictions` (object): The predictions. 
