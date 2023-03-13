from lolpop.component.data_profiler.abstract_data_profiler import AbstractDataProfiler
from lolpop.utils import common_utils as utils
from evidently.report import Report
from evidently.metric_preset import DataQualityPreset, DataDriftPreset
from evidently.test_suite import TestSuite
from evidently.test_preset import DataQualityTestPreset, DataDriftTestPreset, DataStabilityTestPreset

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class EvidentlyAIDataProfiler(AbstractDataProfiler): 
    __REQUIRED_CONF__ = {
        "config" : ["local_dir"]
    }

    def profile_data(self, data, **kwargs): 
        data_report = Report(metrics=[DataQualityPreset()])
        data_report.run(current_data=data, reference_data=None)
        file_path = "%s/EVIDENTLY_DATA_PROFILE_REPORT.HTML" %self._get_config("local_dir")
        data_report.save_html(file_path)
        
        return data_report, file_path

    def compare_data(self, data, prev_data, **kwargs): 
        data_report = None
        file_path = None 
        (data, prev_data, ok) = utils.compare_data_schemas(self, data, prev_data)
        if ok: 
            #data_comparison = TestSuite(tests=[DataStabilityTestPreset(), DataDriftTestPreset()]) #getting errors w/ the testsuite
            data_comparison = Report(metrics=[DataDriftPreset()])
            data_comparison.run(reference_data=prev_data, current_data=data)
            file_path = "%s/EVIDENTLY_DATA_COMPARISON_REPORT.html" %self._get_config("local_dir")
            data_comparison.save_html(file_path)

        return data_report, file_path