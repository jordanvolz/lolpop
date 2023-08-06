from lolpop.component.data_profiler.base_data_profiler import BaseDataProfiler
from lolpop.utils import common_utils as utils
from ydata_profiling import ProfileReport
from ydata_profiling.visualisation.plot import timeseries_heatmap

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class YDataProfilingDataProfiler(BaseDataProfiler): 
    
    __REQUIRED_CONF__ = {
        "config" : ["local_dir"]
    }


    __DEFAULT_CONF__ = {
        "config": {"YDATA_PROFILE_REPORT_NAME": "YDATA_DATA_PROFILE_REPORT.HTML",
                "YDATA_COMPARISON_REPORT_NAME": "YDATA_DATA_COMPARISON_REPORT.HTML"}
    }

    def profile_data(self, data, *args, **kwargs): 
        """Profiles data using Ydata Profiling

        Args:
            data (pd.DataFrame): A dataframe of the data to profile.  

        Returns:
            data_report (object): Python object of the report 
            file_path (string): file path of the exported report
        """
        is_timeseries = self.problem_type == "timeseries"
        data_report = ProfileReport(data, tsmode=is_timeseries)
        file_path = "%s/%s" % (self._get_config("local_dir"),
                               self._get_config("YDATA_PROFILE_REPORT_NAME"))
        data_report.to_file(file_path)
        
        return data_report, file_path

    def compare_data(self, data, prev_data, *args, **kwargs): 
        """Produces a (probably data drift) report between two data sets 
           using Ydata Profiling. 

        Args:
            data (pd.DataFrame): A dataframe of the "current" data. 
            prev_data (pd.DataFrame): A dataframe of the "historical" data. 

        Returns:
            data_report (object): Python object of the report 
            file_path (string): file path of the exported report
        """
        comparison = None 
        file_path = None 
        (data, prev_data, ok) = utils.compare_data_schemas(self, data, prev_data)
        if ok: 
            is_timeseries = self.problem_type == "timeseries"
            profile = ProfileReport(data, tsmode=is_timeseries)
            old_profile = ProfileReport(prev_data, tsmode=is_timeseries)
            comparison = profile.compare(old_profile)
            file_path = "%s/%s" % (self._get_config("local_dir"), self._get_config("YDATA_COMPARISON_REPORT_NAME"))
            comparison.to_file(file_path)

        return comparison, file_path
