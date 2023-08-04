# MetaflowClassificationRunner

The `MetaflowClassificationRunner` class is a subclass of `BaseRunner`. It provides methods to run various pipelines and retrieve artifacts from those pipelines for classification tasks in Metaflow.

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
- `drop_columns`: A list of columns to remove from data before training a model or running inference. 

## Methods

### process_data
Runs the Metaflow process pipeline, retrieves artifacts from the pipeline, and returns the processed data.

```python
def process_data(self, source="train")
```

**Arguments**: 

- `source` (str, optional): The source of data to process. Defaults to "train".

**Returns**: 

- `data` (dataframe): Dataframe with the processed data.
- `dataset_version` (object): The dataset version object.


### train_model
Runs the Metaflow train pipeline, retrieves artifacts from the pipeline, and returns the trained model artifacts.

```python 
train_model(self, data, dataset_version=None)
```

**Arguments**: 

- `data` (dataframe): Dataframe with input features and target variable.
- `dataset_version` (object, optional): The dataset version object. Defaults to None.

**Returns**: 

- `model_version` (dict): Model version information.
- `model` (sklearn.model): Trained model object.
- `is_new_model_better` (bool): Boolean indicating whether the new model is better than the previous model.


### deploy_model 
Runs the Metaflow deploy pipeline, retrieves artifacts from the pipeline, and returns the deployment artifacts.

```python 
def deploy_model(self, model_version, model)
```

**Arguments**: 

- `model_version` (object): Model version object.
- `model` (object): Trained model object.

**Returns**: 


### predict_data 
Runs the Metaflow predict pipeline, retrieves artifacts from the pipeline, and returns the predicted data.

```python 
def predict_data(self, model_version, model, data, dataset_version)
```

**Arguments**: 

- `model_version` (object): Model version object.
- `model` (object, optional): Trained model object. Defaults to None.
- `data` (dataframe): Dataframe with input features.
- `dataset_version` (object): The dataset version object.

**Returns**: 

- `data` (dataframe): Dataframe with predicted data.
- `prediction_job` (object): The prediction job object.


### evaluate_ground_truth 
Evaluates the ground truth and prediction data, calculates metrics, and logs them.

```python
def evaluate_ground_truth(self, prediction_job=None)
```

**Arguments**: 

- `prediction_job` (object, optional): The prediction job object. Defaults to None.


### stop 
Stops the metadata tracker.

```python 
def stop(self)
```



### build_all

Runs the process, train, deploy & evaluation pipelines, retrieves artifacts from the pipelines, and logs the metrics.

```python 
def build_all(self)
```