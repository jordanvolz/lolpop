# OfflineTrain

The `OfflineTrain` class is a subclass of the `BaseTrain` class. It provides methods for performing offline training of a machine learning model. It includes functionality for splitting data into train, validation, and test sets, training the model, performing model checks, analyzing the model, comparing models, checking for model bias, and retraining the model on all available data.
## Configuration 

### Required Configuration 

The `OfflineTrain` requires the following components: 

- `data_splitter`
- `metadata_tracker`
- `resource_version_control`
- `model_explainer`
- `model_checker`
- `model_visualizer`
- `model_bias_checker` 

## Methods

### split_data 
Split the input data into train, validation, and test sets using the configured data splitter.

```python
def split_data(self, data, *args, **kwargs)
```

**Arguments**:

- `data` (object): A DataFrame containing the input data to be split.

**Returns:**

- A dictionary with train, validation, and test data where each is a DataFrame containing the corresponding split.

### train_model 
Train a machine learning model using the input data and return the trained model and model version. If a hyperparameter tuner is configured, it will be used to search for the optimal hyperparameters for the model.

```python 
def train_model(self, data, *args, **kwargs)
```

**Arguments**:

- `data` (object): A dictionary containing train, validation, and test data as returned by the split_data method.

**Returns:**

- A tuple of the trained model and model version.


### check_model 
Perform model checks on the input data and trained model, log the results in the metadata tracker, and notify via email if any issues are found with the checks.

```python 
def check_model(self, data_dict, model, model_version, *args, **kwargs)
```

**Arguments**:

- `data_dict` (object): A dictionary containing train, validation, and test data as returned by the split_data method.
- `model` (object): The trained machine learning model to be checked.
- `model_version` (object): The version of the model being checked.


### analyze_model 
Generate feature importance plots, compare the model and data to a baseline, and generate visualizations to assist in model analysis.

```python 
def analyze_model(self, data_dict, model, model_version, *args, **kwargs)
```

**Arguments**:

- `data_dict` (object): A dictionary containing train, validation, and test data as returned by the split_data method.
- `model` (object): The trained machine learning model to be analyzed.
- `model_version` (object): The version of the model to be analyzed.


### compare_models 
Compare the current model to the previously deployed model, log the comparison results in the metadata tracker, and return a boolean indicating if the current model is an improvement over the previous model.

```python 
def compare_models(self, data_dict, model, model_version, *args, **kwargs)
```

**Arguments**:

- `data_dict` (object): A dictionary containing train, validation, and test data as returned by the split_data method.
- `model` (object): The trained machine learning model to be analyzed.
- `model_version` (object): The version of the model being tested for improvement.

**Returns:**

- A boolean indicating if the current model is an improvement over the previous model. If there is no previous model to compare to, will return True.


### check_model_bias 
Check for bias in the input data and trained model and log the results in the metadata tracker.

```python 
def check_model_bias(self, data_dict, model, model_version, *args, **kwargs)
```


**Arguments**:

- `data_dict` (object): A dictionary containing train, validation, and test data as returned by the split_data method.
- `model` (object): The trained machine learning model to be checked for bias.
- `model_version` (object): The version of the model to be checked for bias.


### retrain_model_on_all_data 
Retrain a machine learning model on all available data and return the new trained model and model version.

```python 
def retrain_model_on_all_data(self, data, model_version, ref_model=None)
```

**Arguments**:

- `data` (object): A DataFrame containing all the data to be used for retraining.
- `model_version` (object): The version of the model to be retrained.
- `ref_model` (object): The previous model to be used as a reference.

**Returns:**

- A tuple of the trained model and model version.
