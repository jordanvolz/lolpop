from component.data_checker.abstract_data_checker import AbstractDataChecker
from utils import common_utils as utils
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import data_integrity

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class DeepchecksDataChecker(AbstractDataChecker): 
    __REQUIRED_CONF__ = {
        "config" : ["local_dir"]
    }
    def check_data(self, data, **kwargs): 
        model_target = self._get_config("MODEL_TARGET")
        label = None 
        if model_target in data.columns:
            label = model_target
            
        ds = Dataset(
            data, 
            label = label, 
            index_name=self._get_config("MODEL_INDEX"), 
            cat_features=self._get_config("MODEL_CAT_FEATURES"), 
            datetime_name=self._get_config("MODEL_TIME_INDEX")
            )
        data_suite = data_integrity() 
        data_report = data_suite.run(ds)
        file_path = "%s/DEEPCHECKS_DATA_REPORT.HTML" %self._get_config("local_dir")
        data_report.save_as_html(file_path)

        checks_status = "PASS"
        if len(data_report.get_not_passed_checks()) > 0: 
            checks_status = "ERROR"
        elif len(data_report.get_not_ran_checks()) > 0: 
            checks_status = "WARN"

        return data_report, file_path, checks_status
