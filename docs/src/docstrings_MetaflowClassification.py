```
The following are the docstrings for the methods in the MetaflowClassificationRunner class.
```

```
__init__(self, problem_type="classification", *args, **kwargs)
```
Initialize the MetaflowClassificationRunner class object.

Args:
- `problem_type` (str, optional): The type of the problem being solved. Defaults to "classification".
- `args`: Variable length argument list.
- `kwargs`: Arbitrary keyword arguments.

```
process_data(self, source = "train")
```
Runs the metaflow process pipeline, retrieves artifacts from the pipeline and returns the processed data. 

Args:
- `source` (str, optional): The source of data to process. Defaults to "train".

Returns:
- `data` (dataframe): Dataframe with the processed data.
- `dataset_version` (dict):  The dictionary of data version information.

```
train_model(self, data, dataset_version=None)
```
Runs the metaflow train pipeline, retrieves artifacts from the pipeline and returns the trained model artifacts. 

Args:
- `data` (dataframe): Dataframe with input features and target variable.
- `dataset_version` (dict, optional): The dictionary of data version information. Defaults to None.

Returns:
- `model_version` (dict): Model version information.
- `model` (sklearn.model): Trained model object.
- `is_new_model_better` (bool): Boolean indicating whether the new model is better than the previous model.

```
deploy_model(self, model_version, model)
```
Runs the metaflow deploy pipeline, retrieves artifacts from the pipeline and returns the deployment artifacts. 

Args:
- `model_version` (dict): Model version information.
- `model` (sklearn.model): Trained model object.

Returns:
- `deployment` (dict): The deployment information.

```
predict_data(self, model_version, model, data, dataset_version)
```
Runs the metaflow predict pipeline, retrieves artifacts from the pipeline and returns the predicted data. 

Args:
- `model_version` (dict): Model version information.
- `model` (sklearn.model, optional): Trained model object. Defaults to None.
- `data` (dataframe): Dataframe with input features.
- `dataset_version` (dict): The dictionary of data version information.

Returns:
- `data` (dataframe): Dataframe with predicted data.
- `prediction_job` (dict): The prediction job information.

```
evaluate_ground_truth(self, prediction_job=None)
```
Evaluates the ground truth and prediction data, calculate metrics and logs them.

Args:
- `prediction_job` (dict, optional): The prediction job information. Defaults to None.

Returns:
- None

```
stop(self)
```
Stops the metadata tracker and has no return value.

Args:
- None

Returns:
- None

```
build_all(self)
```
Runs the process,train,deploy & evaluation pipelines, retrieves artifacts from the pipelines and logs the metrics.

Args:
- None

Returns:
- None