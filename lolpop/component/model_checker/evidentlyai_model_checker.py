from lolpop.component.model_checker.base_model_checker import BaseModelChecker
from lolpop.utils import common_utils as utils
from evidently.test_suite import TestSuite
from evidently.tests import TestColumnDrift
from evidently.report import Report
from evidently.test_preset import MulticlassClassificationTestPreset, NoTargetPerformanceTestPreset, BinaryClassificationTestPreset
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, DataQualityPreset
from evidently import ColumnMapping

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class EvidentlyAIModelChecker(BaseModelChecker): 

    def check_model(self, data_dict, model, **kwargs):
        if self.problem_type == "classification": 
            classification_type = utils.get_multiclass(data_dict["y_train"].unique())

        #set up column mapping 
        column_mapping = ColumnMapping()
        model_target = self._get_config("MODEL_TARGET")
        column_mapping.target = model_target
        column_mapping.prediction = "prediction"

        #set up data + predictions for train/test drift
        df_train, df_test = self.data_splitter.get_train_test_dfs(data_dict) 
        df_train["prediction"] = model._predict_df(df_train.drop([model_target], axis=1))
        df_test["prediction"] = model._predict_df(df_test.drop([model_target], axis=1))

        if self.problem_type == "classification": 
            if classification_type == "multiclass": 
                model_report = TestSuite(tests=[MulticlassClassificationTestPreset(), NoTargetPerformanceTestPreset(), TestColumnDrift(column_name=model_target)])
            else: 
                model_report = TestSuite(tests=[BinaryClassificationTestPreset(), NoTargetPerformanceTestPreset(), TestColumnDrift(column_name=model_target)])
            model_report.run(current_data=df_test, reference_data=df_train, column_mapping=column_mapping)
        else: 
            self.notify("Unsupported problem type: %s" %self.problem_type)
             
        file_path = "%s/EVIDENTLY_MODEL_REPORT.HTML" %self._get_config("local_dir")
        model_report.save_html(file_path)

        summary = model_report.as_dict()["summary"]

        checks_status = "PASS"
        if summary["failed_tests"] > 0: 
            checks_status = "ERROR"
        elif summary["success_tests"] < summary["total_tests"]: 
            checks_status = "WARN"

        return  model_report, file_path, checks_status

    def calculate_model_drift(self, data, current_model, deployed_model):
        #set up dfs
        df_current = data["X_test"].copy() 
        df_deployed = df_current.copy()

        #create column mapping
        column_mapping = ColumnMapping()
        column_mapping.target=self._get_config("model_target")
        column_mapping.target="prediction"
        df_current["prediction"] = current_model._predict_df(df_current)
        df_deployed["prediction"] = deployed_model._predict_df(df_deployed)

        #drift_report = TestSuite(tests=[TestColumnDrift(column_name="prediction")])
        drift_report = Report(metrics = [TargetDriftPreset()])

        drift_report.run(current_data=df_current, reference_data=df_deployed, column_mapping=column_mapping)
        file_path = "%s/EVIDENTLY_MODEL_DRIFT_REPORT.HTML" %self._get_config("local_dir")
        drift_report.save_html(file_path)

        return drift_report, file_path
        