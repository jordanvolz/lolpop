# ClassificationRunner

The `ClassificationRunner` class is a subclass of the `BaseRunner` class and is used for processing, training, deploying, and predicting classification models. This class provides methods for each step of the classification task, including data processing, model training, model deployment, prediction, and evaluation.

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

Processes data and performs transformations, tracking, profiling, checks, and comparisons between different instances of data.

```python 
def process_data(self, source="train", *args, **kwargs)
```

**Arguments**:

- `source` (str):  Indicates the source of the data. Default is "train".

**Returns**:

- `data` (pd.DataFrame): DataFrame version of the processed data.
- `dataset_version` (object): The dataset version object.

### train_model 
Trains the model on the processed data and performs analysis, checks, bias checks, versioning, building lineage, and comparisons between different model versions.

```python 
def train_model(self, data, dataset_version=None, *args, **kwargs)
```
**Arguments**:

- `data` (pd.DataFrame): DataFrame version of the processed data.
- `dataset_version` (object): The dataset version object.

**Returns**:

- `model_version` (object): The model version object.
- `model` (object): The trained model object.
- `is_new_model_better` (bool): Boolean value of whether or not a better model version was trained.

### deploy_model
Deploys the trained model if it is approved.

```python
def deploy_model(self, model_version, model, *args, **kwargs)
```

**Arguments**:

- `model_version` (object): The version of the trained model.
- `model` (object): The trained model object.

**Returns**:

- `deployment` (Any): The model deployment object.

### predict_data
Predicts outcomes for a given dataset using the trained model, and performs data comparison, tracking, drift analysis, and checks.

```python 
def predict_data(self, model_version, model, data, dataset_version, *args, **kwargs)
```

**Arguments**:

- `model_version` (object): The version of the trained model.
- `model` (object): The trained model object.
- `data` (pd.DataFrame): DataFrame version of the dataset to run predictions on.
- `dataset_version` (object): The version of the dataset.

**Returns**:

- `data` (pd.DataFrame): DataFrame version of the dataset with predictions and explanations.
- `prediction_job` (object): The version of the prediction job.

### evaluate_ground_truth 
Evaluates prediction data against actual data.

```python
def evaluate_ground_truth(self, prediction_job=None, *args, **kwargs)
```

**Arguments**:

- `prediction_job` (object): Default is None. The version of the prediction job.

### stop 
Makes sure that all current metadata is saved once the process is stopped.


```python 
def stop(self)
```

### build_all 
Performs all phases of the classification task including data processing, model training, model deployment, prediction, and evaluation, and notifies the user if a new version of the model is better.

```python 
build_all(self)
```

## Usage

```python
from lolpop.runner import ClassificationRunner

# Create a ClassificationRunner object
config_file = "/path/to/config.yaml"
runner = ClassificationRunner(conf=config_file, problem_type="classification")

# Process the training data
data, dataset_version = runner.process_data()

# Train the model on the processed data
model_version, model, is_new_model_better = runner.train_model(data, dataset_version)

# Deploy the trained model
deployment = runner.deploy_model(model_version, model)

# Process the evaluation data
eval_data, eval_dataset_version = runner.process_data(source="eval")

# Predict outcomes for the evaluation data
data, prediction_job = runner.predict_data(model_version, model, eval_data, eval_dataset_version)

# Evaluate prediction data against actual data
runner.evaluate_ground_truth(prediction_job)

# Stop the execution and save metadata
runner.stop()
```

In the above example, a `ClassificationRunner` object is created and used to perform classification tasks. The example demonstrates the complete workflow of processing data, training a model, deploying the model, predicting outcomes, and evaluating the predictions against the actual data.