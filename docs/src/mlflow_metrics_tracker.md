# MLFlowMetricsTracker

The `MLFlowMetricsTracker` class is a subclass of the `BaseMetricsTracker` class. It provides methods for logging and retrieving metrics using the MLFlow tracking library.

## Attributes

The `MLFlowMetricsTracker` class  sets the following attributes in `__init__` and these should generally be considered available when working with the class: 

- `client` : The `mlflow` client. 
- `run` : The current `mlflow` run. 
- `url` : The `mlflow` tracking url. 

## Configuration

### Required Configuration

The `MLFlowMetricsTracker` class requires the following component 

- `metadata_tracker`: This can only be of type `MLFlowMetadataTracker`

### Optional Configuration

The `MLFlowMetricsTracker` class has no optional configuration. 

### Default Configuration 

The `MLFlowMetricsTracker` class has no default configuration. 


## Methods

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
Logs multiple metrics with the corresponding resource ID and specified performance metric.

```python 
def log_metrics(self, resource, metrics, perf_metric, *args, **kwargs)
```


**Arguments**: 

- `resource` (object): A resource object.
- `metrics` (dict): A dictionary containing the metrics.
- `perf_metric` (str): A performance metric.

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


## Usage

```python
from lolpop.component import MLFlowMetricsTracker

config = (
    #insert component config
)

# Initialize MLFlowMetricsTracker
tracker = MLFlowMetricsTracker(conf=config)

# Create a resource object
resource = ...

# Log a metric
metric_id = "loss"
metric_value = 0.5
tracker.log_metric(resource, metric_id, metric_value)

# Retrieve a metric
metric_id = "accuracy"
metric_value = tracker.get_metric(resource, metric_id)
```