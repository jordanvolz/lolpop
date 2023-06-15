# Class AIFairnessModelBiasChecker Documentation
The `AIFairnessModelBiasChecker` class is a subclass of `BaseModelBiasChecker` in the Python package. This class is used for detecting bias in machine learning models and their predictions by using fairness metrics. 

## Methods

### `check_model_bias(self, data, model, *args, **kwargs)` 
Uses the provided data and model to check for bias in the model's predictions.
* `data` - (dict): A dictionary containing the training/testing data.
* `model` - (object): The model trainer object being checked for bias.
Returns:
* `metrics_out` - (dict): A dictionary containing the bias metrics computed by the function.

### `_eval_classes(self, class_list)`
This method evaluates the provided class list and returns it as a new list with evaluated elements. This function is called by the `check_model_bias` function when processing classes for fairness metrics.

## Example Usage

```python
from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from aif360.algorithms.preprocessing import Reweighing
from aif360.algorithms.postprocessing import CalibratedEqOddsPostprocessing 
from aif360.config import DEFAULT_THRESHOLDS
from aif360.algorithms import TransformerFactory

import utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class AIFairnessModelBiasChecker(BaseModelBiasChecker): 

    __REQUIRED_CONF__ = {"config": ["model_target",
                                   "privileged_groups", "unprivileged_groups", 
                                   "favorable_classes", "privileged_classes", 
                                   "protected_attribute_names"]}

    def check_model_bias(self, data, model, *args, **kwargs):
      '''
      Add documentation for the method
      '''
        pass

    def _eval_classes(self, class_list):
        '''
        Add documentation for the method
        '''
        pass

example_dict = {"X_train": df_train, "y_train": df_train[df_target]}
aifc = AIFairnessModelBiasChecker()
result = aifc.check_model_bias(example_dict, model)
``` 
In this code snippet, we instantiate an object of the `AIFairnessModelBiasChecker` class and call the `check_model_bias` method, passing in training and testing data and a model to evaluate. The output of the function is stored in the `result` variable.