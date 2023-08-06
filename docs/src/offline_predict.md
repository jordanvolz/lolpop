# OfflinePredict

The `OfflinePredict` class is a subclass of the `BasePredict` class and provides methods for offline prediction tasks. This class is used to compare data, generate predictions, track predictions, analyze prediction drift, check predictions, and save predictions.

## Configuration 

### Required Configuration 

The `OfflinePredict` requires the following components: 

- `data_connector`
- `metadata_tracker`
- `resource_version_control`
- `model_explainer`
- `data_checker`
- `data_profiler` 

### Optional Configuration 

The `OfflinePredict` uses the following optional configuration:

- `drop_columns`: A list of columns from the dataset to drop before making a prediction. I.E. the columns that are not considered features by the model. 
- `skip_explainer_plots`: Skip generating explainer plots when generating feature importance on the prediction data. 


## Methods

### compare_data 

Given a trained model version, a dataset version, and a data sample, this method compares the current data sample with the training data and logs the report of the comparison to the metadata tracker.

```python 
def compare_data(self, model_version, dataset_version, data, *args, **kwargs)
```

**Arguments**:

- `model_version` (object): The trained model version.
- `dataset_version` (object): The dataset version.
- `data` (pandas.DataFrame): A dataframe containing the data to compare.

**Returns**:

- None

### get_predictions
Given a trained model, a model version, and a data sample, this method returns a pandas dataframe containing predictions and optionally prediction probabilities and explanations. It also logs the prediction metrics to the metrics tracker.

```python 
def get_predictions(self, model, model_version, data, *args, **kwargs)
```

**Arguments**:

- `model` (object): A trained model object.
- `model_version` (object): The model version.
- `data` (pandas.DataFrame): A dataframe containing the data to predict from.

**Returns**:

- A tuple containing the dataframe of predictions and the prediction job object.

### track_predictions 
This method adds a new data sample as a new version to an existing version control resource.

```python 
def track_predictions(self, prediction_job, data, *args, **kwargs)
```

**Arguments**:

- `prediction_job` (object): The prediction job.
- `data` (pandas.DataFrame): A dataframe containing the data to append to the existing version control resource.

**Returns**:

- None

### analyze_prediction_drift 
Given a dataset version, a prediction job, and a data sample, this method analyzes drift in the performance of the model between the current dataset and the previous version. It logs the report of the analysis to the metadata tracker.


```python 
analyze_prediction_drift(self, dataset_version, prediction_job, data, *args, **kwargs)
```

**Arguments**:

- `dataset_version` (object): The dataset version.
- `prediction_job` (object): The prediction job.
- `data` (pandas.DataFrame): A dataframe containing the data to compare.

**Returns**:

- None

### check_predictions 
Given a predicted data sample and a prediction job, this method performs data checks on the data sample and logs the report of the checks to the metadata tracker.

```python
check_predictions(self, data, prediction_job, *args, **kwargs)
```


**Arguments**:

- `data` (pandas.DataFrame): A dataframe of the predicted data.
- `prediction_job` (object): The prediction job.

**Returns**:

- None

### save_predictions 
Given a predicted data sample and the name of a target table, this method saves the data sample to the target table using the data_connector.

```python 
save_predictions(self, data, table, *args, **kwargs)
```


**Arguments**:

- `data` (pandas.DataFrame): A dataframe of the predicted data.
- `table` (str): A string representing the name of the target table.

**Returns**:

- None
