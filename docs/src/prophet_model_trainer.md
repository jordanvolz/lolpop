# ProphetModelTrainer

This is a Python class that inherits from `BaseModelTrainer` and is used to train and predict values using the Prophet model. The class provides methods for fitting the model, making predictions, applying prediction bounds, processing data, and generating plots.

## Configuration 

### Required Configuration

`ProphetModelTrainer` contains the following required configurations: 

- `time_index`: column representing the time index of the model. 
- `model_target`: column representing the model target
- `forecast_frequency`: The frequency of the forecast. I.E. how often predictions are made: `D` for days, `H` for hour, etc. See the prophet documentation for details. 
- `forecast_period`: Length of time of the forecast. This is an integer value of `forecast_frequency` units. 
- `local_dir`: local directory to use to write forecasts.  

### Optional Configuration 
`ProphetModelTrainer` contains the following required configurations: 

- `country_holidays`: Country holiday code to use, if any.  
- `regressor_cols`: List of columns that should be included as additional regressors, if any. 
- `target_min`: minimum value allowed for predictions, if any (i.e. 0)
- `target_max`: maximum value allowed for predictions, if any.

### Default Configuration 
`ProphetModelTrainer` contains no default configuration. 

## Methods

### fit 
Fits the Prophet model to the training data.

```python 
def fit(self, data, *args, **kwargs)
```

**Arguments:**

`data` (dict): Dictionary containing the training data with columns 'X_train' and 'y_train'.

**Returns:**

`model`: A trained Prophet model object.

### predict 
Predicts values for train, validation, and test data.

```python 
def predict(self, data, *args, **kwargs)
```

**Arguments:**

- `data` (dict): A dictionary containing training, validation, and test data with columns 'X_train', 'y_train', 'X_valid', 'y_valid', 'X_test', 'y_test'.

**Returns:**

- `dict`: A dictionary containing predictions for train, validation, and test sets.

### _apply_prediction_bounds
Applies min/max target values to the predicted values.

```python 
def _apply_prediction_bounds(self, data, target_min=None, target_max=None)
```


**Arguments:**

- `data` (pd.DataFrame): DataFrame containing the predicted values.
- `target_min` (float, optional): Minimum permissible value for the predicted values.
- `target_max` (float, optional): Maximum permissible value for the predicted values.

**Returns:**

- `pd.DataFrame`: DataFrame containing the predicted values within the range of [target_min, target_max].

### predict_df 
Predicts values for the given DataFrame.

```python 
def predict_df(self, df, *args, **kwargs) -> pd.DataFrame
```

**Arguments:**
    
- `df` (pd.DataFrame): DataFrame containing the data to be processed.

**Returns:**
    
- `pd.DataFrame`: The predicted values.

### _process_data 
Processes data as per the requirements of the Prophet model.

```python 
def _process_data(self, data) -> pd.DataFrame
```

**Arguments:**

- `data` (pd.DataFrame): DataFrame containing the dataset to be processed.

**Returns:**

- `pd.DataFrame`: The processed dataset.

### get_artifacts 
Generates plots for visualizing the forecasted data.

```python 
get_artifacts(self, id, *args, **kwargs)
```

**Arguments:**

- `id` (str): ID for the model being used for generating plots.

**Returns:**

`dict`: A dictionary containing the paths of the saved plots.

## Usage Example

```python
from lolpop.component import ProphetModelTrainer

... #create data 

# Create an instance of the ProphetModelTrainer class
trainer = ProphetModelTrainer(problem_type='timeseries', params={'seasonality_mode': 'multiplicative'})

# Fit the model to the training data
model = trainer.fit(data={'X_train': train_X, 'y_train': train_y})

# Make predictions for the test data
predictions = trainer.predict(data={'X_test': test_X, 'y_test': test_y})

```
