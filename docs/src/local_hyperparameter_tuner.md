# LocalHyperparameterTuner

This class allows performing hyperparameter tuning with different training parameter configurations to find the best performing model. This class inheriting from the `BaseHyperparameterTuner` class, which implements many standard methods for hyperparameter tuning. 

## Configuration 

This component has no required configuration beyond what is specified in the [BaseHyperparameterTuner](base_hyperparameter_tuner.md) class 

## Methods

### run_experiment 
This method generates a list of experiments by performing hyperparameter tuning with different training parameter configurations. For each configuration, it trains a model, saves it, makes predictions, calculates metrics, and logs the metrics. It then determines the best experiment based on the performance metric, saves the data splits, retrieves the winning experiment and model trainer data, and logs important information to the model version.

```python3
def run_experiment(data, model_version, *args, **kwargs)
```

**Arguments**:

- `data`: A dictionary containing input data for training and testing the model.
- `model_version`: A model_version object from the metadata tracker.

**Returns**:

- `best_model`: The best performing model based on hyperparameter tuning.

**Example**:

```python
from lolpop.component import LocalHyperparameterTuner, LocalDataSplitter, MLFlowMetadataTracker
import pandas as pd 

#get data
data_splitter_config = {
    #insert component config
} 
data_splitter = LocalDataSplitter(conf=data_splitter_config)
df = pd.read_csv("/path/to/data.csv")
data = data_spliter.split_data(df)

#get model_version
metadata_tracker_config = {
    #insert component config here
}
metadata_tracker = MLFlowMetadataTracker(conf=config)
model_version = metadata_tracker.create_resource(id, type="model_version")

config = {
    #insert component config here 

}
# create an instance of LocalHyperparameterTuner
lht = LocalHyperparameterTuner(conf=config)

# run the experiment
best_model = lht.run_experiment(data, model_version)
``` 