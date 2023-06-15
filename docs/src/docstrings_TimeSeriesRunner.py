Class: TimeSeriesRunner

Constructor Method:
    def __init__(self, problem_type="timeseries", *args, **kwargs):
        """
        The constructor method for the TimeSeriesRunner class.

        Args:
            problem_type (str): The problem type for the class. Default is "timeseries".
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.        

        Returns:
            None
        """

Transformation Method:
    def process_data(self, source="train"):
        """
        Method to run data transformation and encoding, track and version data, profile data, run data checks, run data comparison/drift and return transformed data and dataset version.

        Args:
            source (str): The source of the data. It can be either "train" (default) or "eval".

        Returns:
            data (dataset): The transformed dataset
            dataset_version (str): The dataset version.

        """
        
Training Method:
    def train_model(self, data, dataset_version=None):
        """
        Method to split data, train a model, analyze the model, build a model lineage, and compare the new model version to the previous version.

        Args:
            data (dataset): The dataset to train the model on.
            dataset_version (str): The dataset version.

        Returns:
            model_version (str): The model version.
            model (model_object): The trained model object.
            True

        """
Deployment Method:
    def deploy_model(self, model_version, model):
        """
        Method to promote and deploy the latest trained model.

        Args:
            model_version (str): Model version to be deployed.
            model (model_object): The trained model object.

        Returns:
            deployment (deployment_object): The deployed model.

        """
Prediction Method:
    def predict_data(self, model_version, model, data, dataset_version):
        """
        Method to predict data, version data, analyze the prediction drift, and save the predictions.

        Args:
            model_version (str): The version of the model to be used for prediction. 
            model (model_object): The trained model object.
            data (dataset): The dataset for which the predictions need to be obtained.
            dataset_version (str): The dataset version.

        Returns:
            data (dataset): The dataset containing the predictions.
            prediction_job (str): The prediction job ID.

        """
Evaluation Method:
    def evaluate_ground_truth(self, prediction_job=None):
        """
        Method to evaluate the ground truth of the predictions.

        Args:
            prediction_job (str): The prediction job ID.

        Returns:
            None

        """
Stop Method:
    def stop(self):
        """
        Method to stop the metadata tracker.

        Args:
            None

        Returns:
            None

        """
Build All Method:
    def build_all(self):
        """
        Method to process the data, train the model, deploy the trained model, predict the evaluation data, and evaluate the ground truth of the predictions.

        Args:
            None

        Returns:
            None

        """