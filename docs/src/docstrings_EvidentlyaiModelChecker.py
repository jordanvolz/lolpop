```
class EvidentlyAIModelChecker(BaseModelChecker):

    This class is used to check and calculate drift for a trained machine learning model using the EvidentlyAI testing framework. This class inherits BaseModelChecker. 
    
    Methods:
    -----------
    check_model(data_dict, model, **kwargs)
        Check the trained machine learning model for model drift using EvidentlyAI testing framework.

        Parameters:
        -----------
        data_dict : dict
            A dictionary containing training and testing data in the form of pandas dataframes.
        model : object
            A trained machine learning model.
        **kwargs : Arbitrary keyword arguments

        Returns:
        --------
        model_report : object
            A TestSuite Object containing results of model drift tests.
        file_path : str
            The path where the EVIDENTLY_MODEL_REPORT.HTML is stored.
        checks_status : str
            The status of model drift test. It can be "ERROR", "WARN" or "PASS".

    calculate_model_drift(data, current_model, deployed_model)
        Calculate the drift between two trained machine learning models using EvidentlyAI testing framework.

        Parameters:
        -----------
        data : dict
            A dictionary containing training and testing data in the form of pandas dataframes.
        current_model : object
            A trained machine learning model.
        deployed_model : object
            A trained machine learning model.

        Returns:
        --------
        drift_report : object
            A TestSuite Object containing results of model drift tests.
        file_path : str
            The path where the EVIDENTLY_MODEL_DRIFT_REPORT.HTML is stored.
```
Note that the class method decorators have not been added to these docstrings.