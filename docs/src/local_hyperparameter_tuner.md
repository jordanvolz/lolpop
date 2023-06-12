# LocalHyperparameterTuner Class

This class allows performing hyperparameter tuning with different training parameter configurations to find the best performing model. You can take an advantage of the class by inheriting from the `BaseHyperparameterTuner` class.

## `__REQUIRED_CONF__`

- This attribute is a dictionary that specifies the required configuration for the class. If the required configuration is not provided, an exception is raised.

## `run_experiment(data, model_version, *args, **kwargs)`

- This method generate a list of experiments by performing hyperparameter tuning with different training parameter configurations. For each configuration, it trains a model, saves it, makes predictions, calculates metrics, and logs the metrics. It then determines the best experiment based on the performance metric, saves the data splits, retrieves the winning experiment and model trainer data, and logs important information to the model version.

### Arguments

- `data`: A dictionary containing input data for training and testing the model.
- `model_version`: A model_version object from the metadata tracker.
- `*args`: An arbitrary number of positional arguments.
- `**kwargs`: An arbitrary number of keyword arguments.

### Returns

- `best_model`: The best performing model based on hyperparameter tuning.

### Example

``` python
from LocalHyperparameterTuner import LocalHyperparameterTuner

data = {"x_train": x_train, "y_train": y_train , "x_val": x_val, "y_val": y_val}
model_version = ModelVersion("1.0")

# create an instance of LocalHyperparameterTuner
lht = LocalHyperparameterTuner()

# run the experiment
best_model = lht.run_experiment(data, model_version)
``` 

Note: You might need to provide additional arguments to the method depending on the information you need to pass to the `build_model()` method that it calls.