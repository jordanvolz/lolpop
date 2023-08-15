from lolpop.pipeline.predict.base_predict import BasePredict
from lolpop.utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class OfflinePredict(BasePredict): 
    __REQUIRED_CONF__ = {
        "components": ["data_connector", "metadata_tracker", "resource_version_control", "model_explainer", "data_checker", "data_profiler"], 
        "config": []
    }

       
    def compare_data(self, model_version, dataset_version, data, *args, **kwargs):
        """
        Given a trained model version, a dataset version, and a data sample, compares the current 
        data sample with the training data and logs the report of the comparison to the metadata 
        tracker.

        Args:
        model_version(object): The trained model version.
        dataset_version(object): The dataset version.
        data(pandas.DataFrame): A dataframe containing the data to compare.

        Returns:
        None
        """

        #get training dataset version and df 
        vc_info = self.metadata_tracker.get_vc_info(model_version, key="X_train_hexsha")
        train_df = self.resource_version_control.get_data(model_version, vc_info, key = "X_train")

        #compare current dataset version with previous dataset version
        if train_df is not None and not train_df.empty: 
            comparison_report, file_path = self.data_profiler.compare_data(data, train_df)

            self.metadata_tracker.log_data_comparison(
                dataset_version,
                file_path = file_path, 
                report = comparison_report, 
                profiler_class = self.data_profiler.name
                )
        
    def get_predictions(self, model, model_version, data, *args, **kwargs):
        """
        Given a trained model, a model version, and a data sample, returns a pandas dataframe containing 
        predictions and optionally prediction probabilities and explanations, and logs the prediction 
        metrics to the metrics tracker.

        Args:
        model(object): A trained model object.
        model_version(object): The model version.
        data(pandas.DataFrame): A dataframe containing the data to predict from.

        Returns:
        A tuple containing the dataframe of predictions and the unique identifier of the prediction job.
        """

        #get prediction job
        prediction_id = "%s_predictions" %self.metadata_tracker.get_resource_id(model_version)
        prediction_job = self.metadata_tracker.create_resource(id=prediction_id, type="prediction_job", parent=model_version, prediction_count=data.shape[0])

        #drop any metadata columns
        df = data.drop(self._get_config("DROP_COLUMNS", []), axis=1, errors="ignore")

        #make predictions
        data["prediction"] = model.predict_df(df)
        if self.problem_type == "classification": 
            data["prediction_proba"] = model.predict_proba_df(df, to_list=True)

        #get explanations
        if self.problem_type !="timeseries" and not self._get_config("skip_prediction_explanations", False):
            data["explanations"] = self.model_explainer.get_explanations(df, model, model_version, "prediction", to_list=True)

        #log predictions
        self.metrics_tracker.log_prediction_metrics(prediction_job, data["prediction"])

        return data, prediction_job

    def track_predictions(self, prediction_job, data, *args, **kwargs):
        """
        Adds a new data sample as a new version to an existing vc resource.

        Args:
        prediction_job(object): The prediction job.
        data(pandas.DataFrame): A dataframe containing the data to append to the existing vc resource.

        Returns:
        None
        """

        #version data
        vc_info = self.resource_version_control.version_data(prediction_job, data)

        #register version control metadata w/ metadata tracker
        self.metadata_tracker.register_vc_resource(prediction_job, vc_info, file_type="csv")

    def analyze_prediction_drift(self, dataset_version, prediction_job, data, *args, **kwargs):
        """
        Given a dataset version, a prediction job, and a data sample, analyzes drift in the performance 
        of the model between the current dataset and the previous version and logs the report of the 
        analysis to the metadata tracker.

        Args:
        dataset_version(object): The dataset version.
        prediction_job(object): The prediction job.
        data(pandas.DataFrame): A dataframe containing the data to compare.

        Returns:
        None
        """

        #get previous dataset version & dataframe 
        prev_dataset_version = self.metadata_tracker.get_prev_resource_version(dataset_version)
        if prev_dataset_version is not None: 
            vc_info = self.metadata_tracker.get_vc_info(prev_dataset_version)
            prev_data = self.resource_version_control.get_data(prev_dataset_version, vc_info)

            #compare current dataset version with previous dataset version
            if prev_data is not None and not prev_data.empty:
                comparison_report, file_path = self.data_profiler.compare_data(data, prev_data)

                self.metadata_tracker.log_data_comparison(
                    prediction_job,
                    file_path = file_path, 
                    report = comparison_report, 
                    profiler_class = type(self.data_profiler).__name__
                    )
        
    def check_predictions(self, data, prediction_job, *args, **kwargs):
        """
        Given a predicted data sample and a prediction job, performs data checks on the data sample 
        and logs the report of the checks to the metadata tracker.

        Args:
        data(pandas.DataFrame): A dataframe of the predicted data.
        prediction_job(object): The prediction job.

        Returns:
        None
        """
        #run data checks
        data_report, file_path, checks_status = self.data_checker.check_data(data)

        #log data report to metadata tracker
        self.metadata_tracker.log_checks(
            prediction_job,
            file_path = file_path, 
            report = data_report, 
            checker_class = type(self.data_checker).__name__, 
            type = "prediction"
            )

        if checks_status == "ERROR" or checks_status == "WARN": 
            url = self.metadata_tracker.url
            self.notify("Issues found with data checks. Visit %s for more information." %url, checks_status)

    def save_predictions(self, data, table, *args, **kwargs):
        """
        Given a predicted data sample and the name of a target table, saves the data sample to the target 
        table using the data_connector.

        Args:
        data(pandas.DataFrame): A dataframe of the predicted data.
        table(str): A string representing the name of the target table.

        Returns:
        None
        """
        self.data_connector.save_data(data, table)