from lolpop.component.model_checker.base_model_checker import BaseModelChecker
from lolpop.utils import common_utils as utils
from evidently.test_suite import TestSuite
from evidently.tests import TestColumnDrift
from evidently.report import Report
from evidently.test_preset import MulticlassClassificationTestPreset, NoTargetPerformanceTestPreset, BinaryClassificationTestPreset, RegressionTestPreset
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, DataQualityPreset
from evidently import ColumnMapping

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class EvidentlyAIModelChecker(BaseModelChecker): 

    __REQUIRED_CONF__ = {
        "config": ["local_dir", "model_target"]
    }

    __DEFAULT_CONF__ = {
        "config": {"EVIDENTLYAI_MODEL_REPORT_NAME": "EVIDENTLYAI_MODEL_REPORT.HTML",
                   "EVIDENTLYAI_MODEL_DRIFT_REPORT_NAME": "EVIDENTLYAI_MODEL_DRIFT_REPORT.HTML"}
    }

    def check_model(self, data_dict, model, *args, **kwargs):
        """This class is used to check and calculate drift for a trained machine learning model using the EvidentlyAI testing framework. This class inherits BaseModelChecker. 
    
    Methods:
    -----------
    check_model(data_dict, model, **kwargs)
        Runs varies model test presents using EvidentlyAI testing framework.

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
        """
        if self.problem_type == "classification": 
            classification_type = utils.get_multiclass(data_dict["y_train"].unique())

        #set up column mapping 
        column_mapping = ColumnMapping()
        model_target = self._get_config("MODEL_TARGET")
        column_mapping.target = model_target
        column_mapping.prediction = "prediction"
        column_mapping.id = self._get_config("model_index")
        column_mapping.datetime = self._get_config("model_time_index")

        #set up data + predictions for train/test drift
        df_train, df_test = self.data_splitter.get_train_test_dfs(data_dict) 
        df_train["prediction"] = model.predict_df(df_train.drop([model_target], axis=1))
        df_test["prediction"] = model.predict_df(df_test.drop([model_target], axis=1))

        if self.problem_type == "classification": 
            if classification_type == "multiclass": 
                model_report = TestSuite(tests=[MulticlassClassificationTestPreset(), NoTargetPerformanceTestPreset(), TestColumnDrift(column_name=model_target)])
            else: 
                model_report = TestSuite(tests=[BinaryClassificationTestPreset(), NoTargetPerformanceTestPreset(), TestColumnDrift(column_name=model_target)])
        elif self.problem_type == "regression":
            model_report = TestSuite(tests=[RegressionTestPreset(), NoTargetPerformanceTestPreset(), TestColumnDrift(column_name=model_target)])
        else: 
            self.notify("Unsupported problem type: %s" %self.problem_type)
        model_report.run(current_data=df_test, reference_data=df_train, column_mapping=column_mapping)
        file_path = "%s/%s" %(self._get_config("local_dir"), self._get_config("evidentlyai_model_report_name"))
        model_report.save_html(file_path)

        summary = model_report.as_dict()["summary"]

        checks_status = "PASS"
        if summary["failed_tests"] > 0: 
            checks_status = "ERROR"
        elif summary["success_tests"] < summary["total_tests"]: 
            checks_status = "WARN"

        return  model_report, file_path, checks_status

    def calculate_model_drift(self, data, current_model, deployed_model, *args, **kwargs):
        """Calculate the drift between two trained machine learning models using EvidentlyAI testing framework.

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
        """
        #set up dfs
        df_current = data["X_test"].copy() 
        df_deployed = df_current.copy()

        #create column mapping
        column_mapping = ColumnMapping()
        column_mapping.target = check_col_exists(
            self._get_config("MODEL_TARGET"), df_current, df_deployed)
        column_mapping.prediction = "prediction"
        column_mapping.id = check_col_exists(
            self._get_config("model_index"), df_current, df_deployed)
        column_mapping.datetime = check_col_exists(
            self._get_config("model_time_index"), df_current, df_deployed)


        df_current["prediction"] = current_model.predict_df(df_current)
        df_deployed["prediction"] = deployed_model.predict_df(df_deployed)

        #drift_report = TestSuite(tests=[TestColumnDrift(column_name="prediction")])
        drift_report = Report(metrics = [TargetDriftPreset()])

        drift_report.run(current_data=df_current, reference_data=df_deployed, column_mapping=column_mapping)
        file_path = "%s/%s" % (self._get_config(
            "local_dir"), self._get_config("evidentlyai_model_drift_report_name"))
        drift_report.save_html(file_path)

        return drift_report, file_path
        
#drift reports error if one dataset doesn't contain something in the column mapping
# so this ensures we don't get into a mapping that will cause an error.


def check_col_exists(col, dfA, dfB):
    if col in dfA.columns and col in dfB.columns:
        return col
    else:
        return None
