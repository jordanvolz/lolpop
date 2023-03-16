from lolpop.component.data_checker.base_data_checker import BaseDataChecker
from lolpop.utils import common_utils as utils
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import data_integrity

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class DeepchecksDataChecker(BaseDataChecker): 
    
    __REQUIRED_CONF__ = {
        "config" : ["local_dir"]
    }

    def check_data(self, data, *args, **kwargs):
        """Generates a data check report using Deepchecks.

        Args:
            data (pd.DataFrame): A dataframe of the data to check

        Returns:
            data_report (object): Python object of the data report.
            file_path (string):  Path to the exported report. 
            checks_status (string): Status of the checks ("PASS"/"WARN"/"ERROR", etc.)
        """        
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

        num_checks_passed = len(data_report.get_passed_checks())
        num_checks_failed = len(data_report.get_not_passed_checks())
        num_checks_not_ran = len(data_report.get_not_ran_checks())
        self.log("%s had %s passed checks." %(self.name, num_checks_passed))
        self.log("%s had %s failed checks." % (self.name, num_checks_failed))
        self.log("%s had %s checks not run." % (self.name, num_checks_not_ran))

        checks_status = "PASS"
        if num_checks_failed > 0:
            checks_status = "ERROR"
        elif num_checks_not_ran > 0: 
            checks_status = "WARN"

        return data_report, file_path, checks_status
