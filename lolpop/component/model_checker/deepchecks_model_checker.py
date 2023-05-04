from lolpop.component.model_checker.base_model_checker import BaseModelChecker
from lolpop.utils import common_utils as utils
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import model_evaluation
from deepchecks.tabular.checks import TrainTestLabelDrift

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class DeepchecksModelChecker(BaseModelChecker): 

    def check_model(self, data_dict, model, **kwargs): 
        model_target = self._get_config("MODEL_TARGET")
        model_index = self._get_config("MODEL_INDEX")
        model_time_index = self._get_config("MODEL_TIME_INDEX")
        model_cat_features = self._get_config("MODEL_CAT_FEATURES")

        #set up data + predictions for train/text drift
        df_train, df_test = self.data_splitter.get_train_test_dfs(data_dict) 

        ds_train = Dataset(df_train, label = model_target, index_name=model_index, cat_features=model_cat_features, datetime_name=model_time_index)
        ds_test = Dataset(df_test, label = model_target, index_name=model_index, cat_features=model_cat_features, datetime_name=model_time_index)
      
        model_suite = model_evaluation() 
        model_report = model_suite.run(ds_train, ds_test, model._get_model())

        file_path = "%s/DEEPCHECKS_MODEL_REPORT.HTML" %self._get_config("local_dir")
        model_report.save_as_html(file_path)
        
        checks_status = "PASS"
        if len(model_report.get_not_passed_checks()) > 0: 
            checks_status = "ERROR"
        elif len(model_report.get_not_ran_checks()) > 0: 
            checks_status = "WARN"

        return model_report, file_path, checks_status

    def calculate_model_drift(self, data, current_model, deployed_model, **kwargs): 
        model_target = self._get_config("MODEL_TARGET")
        model_index = self._get_config("MODEL_INDEX")
        model_time_index = self._get_config("MODEL_TIME_INDEX")
        model_cat_features = self._get_config("MODEL_CAT_FEATURES")

        df_current = data["X_test"].copy() 
        df_deployed = df_current.copy()
        df_current["prediction"] = current_model._predict_df(df_current)
        df_deployed["prediction"] = deployed_model._predict_df(df_deployed)

        ds_current = Dataset(df_current, label = "prediction", index_name=model_index, cat_features=model_cat_features, datetime_name=model_time_index)
        ds_deployed = Dataset(df_deployed, label = "prediction", index_name=model_index, cat_features=model_cat_features, datetime_name=model_time_index)
      
        check = TrainTestLabelDrift()
        model_report = check.run(train_dataset=ds_deployed, test_dataset=ds_current)

        file_path = "%s/DEEPCHECKS_MODEL_DRIFT_REPORT.HTML" %self._get_config("local_dir")
        model_report.save_as_html(file_path)

        return model_report, file_path

