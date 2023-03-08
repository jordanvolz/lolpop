from pipeline.predict.abstract_predict import AbstractPredict
from utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class OfflinePredict(AbstractPredict): 
    __REQUIRED_CONF__ = {
        "components": ["data_transformer", "metadata_tracker", "resource_version_control", "prediction_explainer", "prediction_checker"], 
        "config": []
    }

    def __init__(self, conf, runner_conf, **kwargs): 
        super().__init__(conf, runner_conf, **kwargs)
        
    def compare_data(self, model_version, dataset_version, data):
        #get training dataset version and df 
        vc_info = self.metadata_tracker.get_vc_info(model_version, key="git_hexsha_train_csv")
        train_df = self.resource_version_control.get_data(model_version, vc_info, key = "train_csv")

        #compare current dataset version with previous dataset version
        comparison_report, file_path = self.data_profiler.compare_data(data, train_df)

        self.metadata_tracker.log_data_comparison(
            dataset_version,
            file_path = file_path, 
            report = comparison_report, 
            profiler_class = type(self.data_profiler).__name__
            )
        
    def get_predictions(self, model, model_version, data): 
        #get prediction job
        prediction_job = self.metadata_tracker.create_resource(id=None, type="prediction_job")

        #make predictions
        data["predictions"] = model._predict_df(data)

        #get explanations
        data["explanations"] = self.prediction_explainer.get_explanations(data, model, model_version, "predictions", to_list=True)

        #log predictions
        self.metrics_tracker.log_prediction_metrics(prediction_job, data["predictions"])

        return data, prediction_job

    def track_predictions(self, prediciton_job, data):
        #version data
        vc_info = self.resource_version_control.version_data(prediciton_job, data)

        #register version control metadata w/ metadata tracker
        self.metadata_tracker.register_vc_resource(prediciton_job, vc_info, key="data_csv", file_type="csv")

    def analyze_prediction_drift(self, dataset_version, prediction_job, data):
        #get previous dataset version & dataframe 
        prev_dataset_version = self.metadata_tracker.get_prev_resource_version(dataset_version)
        vc_info = self.metadata_tracker.get_vc_info(prev_dataset_version)
        prev_data = self.resource_version_control.get_data(prev_dataset_version, vc_info, key = "data_csv")

        #compare current dataset version with previous dataset version
        comparison_report, file_path = self.prediction_profiler.compare_data(data, prev_data)

        self.metadata_tracker.log_data_comparison(
            prediction_job,
            file_path = file_path, 
            report = comparison_report, 
            profiler_class = type(self.data_profiler).__name__
            )
        
    def check_predictions(self, data, prediction_job): 
        #run data checks
        data_report, file_path, checks_status = self.prediction_checker.check_data(data)

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

    def save_predictions(self, data): 
        self.data_transformer.save_data(data)