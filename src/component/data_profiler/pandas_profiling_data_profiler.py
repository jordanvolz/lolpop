from component.data_profiler.abstract_data_profiler import AbstractDataProfiler
from utils import common_utils as utils
from ydata_profiling import ProfileReport

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class PandasProfilingDataProfiler(AbstractDataProfiler): 
    __REQUIRED_CONF__ = {
        "config" : ["local_dir"]
    }

    def profile_data(self, data, **kwargs): 
        data_report = ProfileReport(data)
        file_path =  "%s/PANDAS_PROFILING_DATA_PROFILE_REPORT.html" %self._get_config("local_dir")
        data_report.to_file(file_path)
        
        return data_report, file_path

    def compare_data(self, data, prev_data, **kwargs): 
        comparison = None 
        file_path = None 
        (data, prev_data, ok) = utils.compare_data_schemas(self, data, prev_data)
        if ok: 
            profile = ProfileReport(data)
            old_profile = ProfileReport(prev_data)
            comparison = profile.compare(old_profile)
            file_path =  "%s/PANDAS_PROFILING_DATA_COMPARISON_REPORT.html" %self._get_config("local_dir")
            comparison.to_file(file_path)

        return comparison, file_path
