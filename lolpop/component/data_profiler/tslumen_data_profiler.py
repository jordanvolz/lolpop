from lolpop.component.data_profiler.base_data_profiler import BaseDataProfiler
from lolpop.utils import common_utils as utils
from tslumen import HtmlReport

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class tslumenDataProfiler(BaseDataProfiler):

    __REQUIRED_CONF__ = {
        "config": ["local_dir"]
    }

    __DEFAULT_CONF__ = {
        "config": {"TSLUMEN_PROFILE_REPORT_NAME": "TSLUMEN_DATA_PROFILE_REPORT.HTML"}
    }

    def profile_data(self, data, *args, **kwargs):
        """Profiles data using tslumen

        Args:
            data (pd.DataFrame): A dataframe of the data to profile.  

        Returns:
            data_report (object): Python object of the report 
            file_path (string): file path of the exported report
        """
        ts_data = data.set_index(self._get_config("time_index"))
        if ts_data.index.inferred_freq is None: 
            ts_data = ts_data.asfreq(self._get_config("forecast_frequency"))
        data_report = HtmlReport(ts_data)
        file_path = "%s/%s" %(self._get_config("local_dir"), self._get_config("TSLUMEN_PROFILE_REPORT_NAME"))
        data_report.save(file_path)

        return data_report, file_path