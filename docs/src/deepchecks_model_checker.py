# **Class: DeepchecksModelChecker**

The `DeepchecksModelChecker` class is a subclass of the `BaseModelChecker` class. This class provides methods to check a model against data, save the Deepchecks model suite report in HTML format, and compare the performance of two models on data.

## Methods
The following are the methods that are available in the `DeepchecksModelChecker` class:

### check_model(data_dict, model, **kwargs)
This method checks the given model against the provided data dict and returns the model suite report, file path of the saved HTML file, and the status of the checks.

#### Parameters
- `data_dict` (dictionary): The dictionary containing data for the model.
- `model` (object): The object of the model class.

#### Returns
- `model_report` (object): The model suite report.
- `file_path` (str): The location of the saved HTML file.
- `checks_status` (str): The status (PASS, ERROR or WARN) of model checks.

#### Examples
```python
checker = DeepchecksModelChecker(config={"local_dir": "/path/to/directory"})
data_dict = {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}
model = Model()
model_report, file_path, checks_status = checker.check_model(data_dict, model)

print(checks_status)
```

### calculate_model_drift(data, current_model, deployed_model, **kwargs)
This method compares the performance of two models on the given data and returns the train/test drift report object and file path of the saved HTML file.

#### Parameters
- `data` (dictionary): The dictionary containing data for the models.
- `current_model` (object): The current state model object.
- `deployed_model` (object): The already deployed model object.

#### Returns
- `model_report` (object): The train/test drift report object.
- `file_path` (str): The location of the saved HTML file.

#### Examples
```python
checker = DeepchecksModelChecker(config={"local_dir": "/path/to/directory"})
data = {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}
current_model = Model()
deployed_model = Model()

model_report, file_path = checker.calculate_model_drift(data, current_model, deployed_model)

print(model_report.get_all_checks())
```