# TimeSeriesRunner

The `TimeSeriesRunner` class is a subclass of the `BaseRunner` class and is used for running time series data pipelines. This class provides methods for processing data, training models, deploying models, predicting data, evaluating ground truth, stopping the metadata tracker, and building all components.


## Configuration 

### Required Configuration

The `ClassificationRunner` class requires the following pipelines:

- `process`
- `train`
- `deploy`
- `predict`

and the following components: 

- `metadata_tracker`
- `metrics_tracker`
- `resource_version_control`

and the following configuration: 

- `train_data`: The training data set. This could be a path to the data or a table name, etc.
- `eval_data`:  The evaluation data set. This could be a path to the data or a table name, etc.
- `prediction_data`: The prediction data set. This could be a path to the data or a table name, etc.
- `model_target`: The column name that corresponds to the model target. 
- `time_index`: The column name that corresponds to the time index.  


## Methods

### process_data
This method runs data transformation and encoding, tracks and versions data, profiles data, runs data checks, runs data comparison/drift, and returns transformed data and dataset version.

```python 
process_data(self, source="train", *args, **kwargs)
```

**Arguments**:

- `source` (str): The source of the data. It can be either "train" (default) or "eval".

**Returns**:

- `data` (object): The transformed dataset.
- `dataset_version` (object): The dataset version.

### train_model 
This method splits data, trains a model, analyzes the model, builds a model lineage, and compares the new model version to the previous version.

```python 
def train_model(self, data, dataset_version=None, *args, **kwargs)
```

**Arguments**:

- `data` (object): The dataset to train the model on.
- `dataset_version` (object): The dataset version.

**Returns**:

- `model_version` (object): The model version.
- `model` (object): The trained model object.
- `True`

### deploy_model 
This method promotes and deploys the latest trained model.

```python 
def deploy_model(self, model_version, model, *args, **kwargs)
```

**Arguments**:

- `model_version` (str): Model version to be deployed.
- `model` (object): The trained model object.

**Returns**:

- `deployment` (object): The deployed model.

### predict_data 
This method predicts data, versions data, analyzes the prediction drift, and saves the predictions.

```python
def predict_data(self, model_version, model, data, dataset_version, *args, **kwargs)
```

**Arguments**:

- `model_version` (object): The version of the model to be used for prediction.
- `model` (object): The trained model object.
- `data` (object): The dataset for which the predictions need to be obtained.
- `dataset_version` (object): The dataset version.

**Returns**:

- `data` (object): The dataset containing the predictions.
- `prediction_job` (object): The prediction job ID.

### evaluate_ground_truth 

```python 
def evaluate_ground_truth(self, prediction_job=None, *args, **kwargs)
```
This method evaluates the ground truth of the predictions.

**Arguments**:

- `prediction_job` (str): The prediction job ID.

**Returns**:

- `None`

### stop 

This method stops the metadata tracker.

```python
def stop(self)
```

### build_all 
This method processes the data, trains the model, deploys the trained model, predicts the evaluation data, and evaluates the ground truth of the predictions.

```python 
def build_all(self, *args, **kwargs)
```

## Usage 

```python
from lolpop.runner import TimeSeriesRunner() 

# Create an instance of the TimeSeriesRunner class
config_file = "/path/to/config.yaml"
runner = TimeSeriesRunner(conf=config_file)

# Process the data
data, dataset_version = runner.process_data()

# Train the model
model_version, model, is_new_model_better = runner.train_model(data, dataset_version)

# Deploy the trained model
deployment = runner.deploy_model(model_version)

# Predict the evaluation data
eval_data, eval_dataset_version = runner.process_data(source="eval")
data, prediction_job = runner.predict_data(model_version, model, eval_data, eval_dataset_version)

# Evaluate the ground truth of the predictions
runner.evaluate_ground_truth(prediction_job)

# Stop the metadata tracker
runner.stop()

```

In the example above, we create an instance of the `TimeSeriesRunner` class and use its methods to process data, train a model, deploy the model, predict data, evaluate ground truth, stop the metadata tracker, and build all components.