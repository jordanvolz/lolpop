class OfflinePredict:
    """
    A class for performing offline predictions and analyzing model performance. 

    Attributes:
    problem_type(str): A string indicating the type of problem the model aims to solve. Can take values 
        "regression", "classification", or "timeseries"

    Methods:
    compare_data(model_version:str, dataset_version:str, data:pandas.DataFrame) -> None:
        Given a trained model version, a dataset version, and a data sample, compares the current 
        data sample with the training data and logs the report of the comparison to the metadata 
        tracker.

    get_predictions(model:Model, model_version:str, data:pandas.DataFrame) -> Tuple[pandas.DataFrame,str]:
        Given a trained model, a model version, and a data sample, returns a pandas dataframe containing 
        predictions and optionally prediction probabilities and explanations, and logs the prediction 
        metrics to the metrics tracker.

    track_predictions(prediction_job:str, data:pandas.DataFrame) -> None:
        Adds a new data sample as a new version to an existing vc resource.

    analyze_prediction_drift(dataset_version:str, prediction_job:str, data:pandas.DataFrame) -> None:
        Given a dataset version, a prediction job, and a data sample, analyzes drift in the performance 
        of the model between the current dataset and the previous version and logs the report of the 
        analysis to the metadata tracker.

    check_predictions(data:pandas.DataFrame, prediction_job:str) -> None:
        Given a predicted data sample and a prediction job, performs data checks on the data sample 
        and logs the report of the checks to the metadata tracker.

    save_predictions(data:pandas.DataFrame, table:str) -> None:
        Given a predicted data sample and the name of a target table, saves the data sample to the target 
        table using the data_connector.
    """

    def compare_data(self, model_version:str, dataset_version:str, data:pandas.DataFrame) -> None:
        """
        Given a trained model version, a dataset version, and a data sample, compares the current 
        data sample with the training data and logs the report of the comparison to the metadata 
        tracker.

        Args:
        model_version(str): A string representing the unique identifier of the trained model version.
        dataset_version(str): A string representing the unique identifier of the dataset version.
        data(pandas.DataFrame): A dataframe containing the data to compare.

        Returns:
        None
        """
        pass
        
    def get_predictions(self, model:Model, model_version:str, data:pandas.DataFrame) -> Tuple[pandas.DataFrame,str]:
        """
        Given a trained model, a model version, and a data sample, returns a pandas dataframe containing 
        predictions and optionally prediction probabilities and explanations, and logs the prediction 
        metrics to the metrics tracker.

        Args:
        model(Model): A trained model object.
        model_version(str): A string representing the unique identifier of the model version.
        data(pandas.DataFrame): A dataframe containing the data to predict from.

        Returns:
        A tuple containing the dataframe of predictions and the unique identifier of the prediction job.
        """
        pass

    def track_predictions(self, prediction_job:str, data:pandas.DataFrame) -> None:
        """
        Adds a new data sample as a new version to an existing vc resource.

        Args:
        prediction_job(str): A string representing the unique identifier of the prediction job.
        data(pandas.DataFrame): A dataframe containing the data to append to the existing vc resource.

        Returns:
        None
        """
        pass

    def analyze_prediction_drift(self, dataset_version:str, prediction_job:str, data:pandas.DataFrame) -> None:
        """
        Given a dataset version, a prediction job, and a data sample, analyzes drift in the performance 
        of the model between the current dataset and the previous version and logs the report of the 
        analysis to the metadata tracker.

        Args:
        dataset_version(str): A string representing the unique identifier of the dataset version.
        prediction_job(str): A string representing the unique identifier of the prediction job.
        data(pandas.DataFrame): A dataframe containing the data to compare.

        Returns:
        None
        """
        pass

    def check_predictions(self, data:pandas.DataFrame, prediction_job:str) -> None:
        """
        Given a predicted data sample and a prediction job, performs data checks on the data sample 
        and logs the report of the checks to the metadata tracker.

        Args:
        data(pandas.DataFrame): A dataframe of the predicted data.
        prediction_job(str): A string representing the unique identifier of the prediction job.

        Returns:
        None
        """
        pass

    def save_predictions(self, data:pandas.DataFrame, table:str) -> None:
        """
        Given a predicted data sample and the name of a target table, saves the data sample to the target 
        table using the data_connector.

        Args:
        data(pandas.DataFrame): A dataframe of the predicted data.
        table(str): A string representing the name of the target table.

        Returns:
        None
        """
        pass