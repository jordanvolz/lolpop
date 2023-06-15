Here are the docstrings for all the methods in the given class:

```
class AlibiModelExplainer(BaseModelExplainer):
    This is a class for generating feature importance metrics for a given machine learning (ML) model. It allows us to generate SHAP-based feature importance scores and the related plots. 

    Methods:
    
    __init__(self, problem_type, data_splitter, metadata_tracker, *args, **kwargs):
        This is the constructor of the class. It initializes a new instance of the AlibiModelExplainer class.

        Args:
        problem_type (str): The type of problem we are trying to solve. It can be either "classification" or "regression".
        data_splitter (object): An object that can split data into train and test sets.
        metadata_tracker (object): An object that can track metadata.
        args: Additional unnamed arguments.
        kwargs: Additional named arguments.

    get_explanations(self, data, model, model_version, label, classification_type=None, to_list=False, skip_explainer_plots=True, *args, **kwargs):
        This method generates SHAP-based feature importance scores for a given model and input data. If skip_explainer_plots is True, only the feature importance scores will be returned in Alibi format. If it is False, the method will save the SHAP summary and dependence plots as artifacts.

        Args:
        data (pandas.DataFrame): The input data to explain the model.
        model (object): The machine learning model we wish to explain.
        model_version (string): The version of the machine learning model we wish to explain.
        label (string): A label given to the data.
        classification_type (string): The type of classification. This parameter is only used if the problem type is classification. 
        to_list (boolean): If True the returned explanations will be in a list format.
        skip_explainer_plots (boolean): If True, the skip the SHAP plots.
        args: Additional unnamed arguments.
        kwargs: Additional named arguments.

        Returns:
        A dictionary containing SHAP explainer and SHAP values.

    get_feature_importance(self, data_dict, model, model_version, *args, **kwargs):
        This method generates SHAP-based feature importance scores for train and test sets. It saves SHAP summary and dependence plots as artifacts. 

        Args:
        data_dict (dict): A dictionary of the input data to explain.
        model (object): The machine learning model we wish to explain.
        model_version (string): The version of the machine learning model we wish to explain.
        args: Additional unnamed arguments.
        kwargs: Additional named arguments.

        Returns:
        Tuple of two Alibi data objects:
        - the SHAP-based feature importance for the training set.
        - the SHAP-based feature importance for the test set.

    _get_shap_plots(self, shap_values, expected_value, data, model, label, model_version, classification_type=None):
        This method generates various SHAP plots for the given SHAP values and saves them as artifacts.

        Args:
        shap_values (numpy.ndarray): The SHAP values to generate the plots.
        expected_value (float): The expected value of the model.
        data (pandas.DataFrame): The input data to the model.
        model (object): The machine learning model to explain.
        label (string): A label for the data.
        model_version (string): The version of the model to explain.
        classification_type (string): The type of classification.

        Returns:
        None.

    _save_pyplot(self, name, label, model_version):
        This method saves the generated SHAP plot as an artifact.

        Args:
        name (string): A name for the plot.
        label (string): The label of the data.
        model_version (string): The version of the model to explain.

        Returns:
        The saved artifact.

    _save_file(self, name, label, content, model_version, extension="html"):
        This method saves the generated SHAP plot to a file as an artifact.

        Args:
        name (string): A name for the file.
        label (string): The label of the data.
        content (string): The content of the file.
        model_version (string): The version of the model to explain.
        extension (string): The extension of the file.

        Returns:
        The saved artifact.

    _compare_train_test_feat_importance(self, explanations_train, explanations_test, classification_type, threshold=0.25):
        This method compares the SHAP-based feature importance scores between the train and test sets. 

        Args:
        explanations_train (pandas.DataFrame): The SHAP-based feature importance for the training set.
        explanations_test (pandas.DataFrame): The SHAP-based feature importance for the test set.
        classification_type (string): The type of classification.
        threshold (float): A threshold value for checking the differences between train and test sets.

        Returns:
        Tuple containing the expected differences and the feature importance differences.
```
