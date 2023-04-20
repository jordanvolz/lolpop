from lolpop.component.data_profiler.base_data_profiler import BaseDataProfiler
from lolpop.utils import common_utils as utils
import sweetviz as sv

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class SweetvizDataProfiler(BaseDataProfiler): 
    
    __REQUIRED_CONF__ = {
        "config" : ["local_dir", "model_target"]
    }

    def profile_data(self, data, *args, **kwargs): 
        """Profiles data using Sweetviz

        Args:
            data (pd.DataFrame): A dataframe of the data to profile.  

        Returns:
            data_report (object): Python object of the report 
            file_path (string): file path of the exported report
        """
        model_target = self._get_config("model_target")
        feat_cfg = sv.FeatureConfig(force_num=[model_target]) #sv only supports numeric and boolean targets, so we may as well just force all categorical to be numeric
        data_report = sv.analyze(data, target_feat = model_target, feat_cfg = feat_cfg)
        file_path =  "%s/SWEETVIZ_DATA_PROFILE_REPORT.html" %self._get_config("local_dir")
        data_report.show_html(filepath = file_path, open_browser=False) 
        
        return data_report, file_path

    def compare_data(self, data, prev_data, *args, **kwargs): 
        """Produces a (probably data drift) report between two data sets 
           using Sweetviz. 

        Args:
            data (pd.DataFrame): A dataframe of the "current" data. 
            prev_data (pd.DataFrame): A dataframe of the "historical" data. 

        Returns:
            data_report (object): Python object of the report 
            file_path (string): file path of the exported report
        """
        model_target = self._get_config("model_target")
        feat_cfg = sv.FeatureConfig(force_num=[model_target]) 
        data_report = sv.compare([data, "Current Data"], [prev_data, "Previous Data"], target_feat = model_target, feat_cfg = feat_cfg)
        file_path =  "%s/SWEETVIZ_DATA_COMPARISON_REPORT.html" %self._get_config("local_dir")
        data_report.show_html(filepath = file_path, open_browser=False) 

        return data_report, file_path

