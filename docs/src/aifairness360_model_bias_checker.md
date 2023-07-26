# AIFairnessModelBiasChecker

The `AIFairnessModelBiasChecker` class is a subclass of `BaseModelBiasChecker` in the Python package. This class is used for detecting bias in machine learning models and their predictions by using fairness metrics. 

## Configuration

### Required Configuration
The AIFairness model bias checker requires the following configuration: 

- `model_target`: The model target, or label. 
- `favorable_classes`: values of the `model_target` that are considered favorable.
- `protected_attribute_names`: The features that you want to check for bias.
- `privileged_classes`: Values of the `protected_attribute_names` that you believe might be privileged. 
- `privileged_groups`: List of groups to consider privileged.
- `unprivileged_groups`: List of groups to consider unprivileged.

### Optional Configuration
The AIFairness model bias checker has no optional configuration.

### Default Configuration
The AIFairness model bias checker has no default configuration.

### Sample Configuration 

```yaml 
  model_bias_checker: 
    config: 
        #the features that you want to check bias on
        protected_attribute_names : ["GENDER", "VACCINATED", "STERILIZED"] 
        # the values of the target variable that are considered good/favorable
        favorable_classes : [0,1]
        # the values of the protected_attribute_names that you believe may be privileged. 
        # Same order as above and each column can take a list of values
        # this should be something like [[1],[1],[1]] 
        privileged_classes:  [[1],[1],[1]]
        # list of groups to consider privilege/unprivilege. 
        # Each "group" is a dict of values of protected_attributes
        # 'AND' logic is applied between members of a dict, and 'OR' between dicts in the list
        #GENDER=1 AND VACCINATED=1 AND STERILIZED=1
        privileged_groups :   [{"GENDER" : 1, "VACCINATED":1, "STERILIZED":1}] 
        #GENDER=0 OR VACCINATED=0 OR STERILIZED=0
        unprivileged_groups : [{"GENDER" : 0}, {"VACCINATED":0}, {"STERILIZED":0}] 
```
## Methods

### check_model_bias 
Uses the provided data and model to check for bias in the model's predictions.

```python 
def check_model_bias(self, data, model, *args, **kwargs)
```

**Arguments**: 

* `data` (dict): A dictionary containing the training/testing data.
* `model` (object): The model trainer object being checked for bias.

**Returns**:

* `metrics_out` (dict): A dictionary containing the bias metrics computed by the function.

### _eval_classes
This method evaluates the provided class list and returns it as a new list with evaluated elements. This function is called by the `check_model_bias` function when processing classes for fairness metrics.

```python 
def _eval_classes(self, class_list)
```
Helper function that evalutes `lambda` function defined in configuration into proper python functions. 

**Arguments**: 

* `class_list` (list): A dictionary containing the training/testing data.

**Returns**:

* `class_list` (list): A dictionary containing the training/testing data.


## Usage

```python
from lolpop.component import AIFairnessModelBiasChecker
import pandas as pd 

#get data
data_splitter_config = {
    #insert component config
} 
data_splitter = LocalDataSplitter(conf=data_splitter_config)
df = pd.read_csv("/path/to/data.csv")
data = data_spliter.split_data(df)

#get model
hpt_config = {
    #insert component config here 

}
oht = OptunaHyperparameterTuner(conf=hpt_config)
model = oht.run_experiment(data, model_version)

config = {
  #insert component config here
}
aifmbc = AIFairnessModelBiasChecker(conf=config)
bias_metrics = aifc.check_model_bias(data, model)
``` 
