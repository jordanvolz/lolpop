# XGBoostModelTrainer

The `XGBoostModelTrainer` class is a subclass of the `BaseModelTrainer` class. It provides functionality for training and predicting using XGBoost models. XGBoost is an optimized gradient boosting library that is popularly used for machine learning tasks.

## Configuration

`XGBoostModelTrainer` has no additional configuration beyond what is required in [BaseModelTrainer](base_model_trainer.md)

## Methods

### fit 
This method trains the XGBoost model on the given data.

```python 
def fit(self, data, *args, **kwargs)
```

**Arguments**:

- `data` (dict): Dictionary containing input features `X_train`, `y_train`, `X_valid`, and `X_test`.


**Returns**:

- `model`: XGBoost model object.

### predict 
This method performs prediction using the trained XGBoost model.

```python
def predict(self, data, *args, **kwargs)
```

**Arguments**:

- `data` (dict): Dictionary containing input features `X_train`, `y_train`, `X_valid`, and `X_test`.
- `*args`, `**kwargs`: Additional arguments and keyword arguments.

**Returns**:

- `dict`: Dictionary containing train, valid, and test predictions and probabilities if applicable.

### predict_df 
This method performs prediction using the trained XGBoost model on a pandas DataFrame.

```python
def predict_df(self, df, *args, **kwargs)
```
**Arguments**:

- `df` (pandas DataFrame): DataFrame containing input features.

**Returns**:

- `numpy array`: Predicted output.

### predict_proba_df 
This method performs prediction probabilities estimation of the trained XGBoost model on a pandas DataFrame.

```python 
predict_proba_df(self, df, to_list=False, *args, **kwargs)
```

**Arguments**:

- `df` (pandas DataFrame): DataFrame containing input features.
- `to_list` (bool): Whether to convert the probabilities into a list.

**Returns**:

- `numpy array` or `list`: Predicted probabilities.

## Usage

```python
from lolpop.component import XGBoostModelTrainer 

... # create datasets

data = {
    "X_train": X_train,
    "y_train": y_train,
    "X_valid": X_valid,
    "X_test": X_test
}

trainer = XGBoostModelTrainer(problem_type="classification", params={"n_estimators": 100})

# Train the XGBoost model
trained_model = trainer.fit(data)

# Perform prediction
predictions = trainer.predict(data)
```
In the example above, an instance of the `XGBoostModelTrainer` class is created with a problem type of "classification" and the number of estimators set to 100. The `fit` method is then used to train the model on the given data. Finally, the `predict` method is used to make predictions based on the trained model.