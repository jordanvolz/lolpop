from lolpop.component.data_checker.base_data_checker import BaseDataChecker
from lolpop.utils import common_utils as utils
from evidently.test_suite import TestSuite
from evidently.test_preset import *

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class EvidentlyAIDataChecker(BaseDataChecker): 
    
    __REQUIRED_CONF__ = {
        "config" : ["local_dir"]
    }

    def check_data(self, data, *args, **kwargs): 
        """Generates a data check report using EvidentlyAI.

        Args:
            data (pd.DataFrame): A dataframe of the data to check

        Returns:
            data_report (object): Python object of the data report.
            file_path (string):  Path to the exported report. 
            checks_status (string): Status of the checks ("PASS"/"WARN"/"ERROR", etc.)
        """
        data_report = TestSuite(tests=[DataQualityTestPreset()])
        data_report.run(current_data=data, reference_data=None)
        file_path = "%s/EVIDENTLY_DATA_REPORT.HTML" %self._get_config("local_dir")
        data_report.save_html(file_path)

        summary = data_report.as_dict()["summary"]
        
        num_checks_passed = summary["success_tests"]
        num_checks_failed = summary["failed_tests"]
        num_checks_not_ran = summary["total_tests"] - (num_checks_failed + num_checks_passed)
        self.log("%s had %s passed checks." % (self.name, num_checks_passed))
        self.log("%s had %s failed checks." % (self.name, num_checks_failed))
        self.log("%s had %s checks not run." % (self.name, num_checks_not_ran))

        checks_status = "PASS"
        if num_checks_failed > 0: 
            checks_status = "ERROR"
        elif num_checks_not_ran > 0: 
            checks_status = "WARN"

        return data_report, file_path, checks_status
