from pipeline.process.abstract_process import AbstractProcess
from utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class OfflineProcess(AbstractProcess): 
    __REQUIRED_CONF__ = {
        "components": ["data_transformer", "metadata_tracker", "resource_version_control", "data_profiler", "data_checker"], 
        "config": []
    }

    def __init__(self, conf, runner_conf, **kwargs): 
        super().__init__(conf, runner_conf, **kwargs)

    def transform_data(self, source_table_name): 
        #get source data
        data = self.data_transformer.get_data(source_table_name)

        #transform data
        data_out = self.data_transformer.transform(data, source_table_name)

        return data_out

    def track_data(self, data, id): 
        #create dataset version 
        dataset_version = self.metadata_tracker.create_resource(id, type="dataset_version")
        self.datasets_used.append(dataset_version)
        
        #version data
        vc_info = self.resource_version_control.version_data(dataset_version, data)

        #register version control metadata w/ metadata tracker
        self.metadata_tracker.register_vc_resource(dataset_version, vc_info, key="data_csv", file_type="csv")

        return dataset_version
      
    def profile_data(self, data, dataset_version): 
        #profile data
        data_profile, file_path = self.data_profiler.profile_data(data)

        #log profile to metadata tracker
        self.metadata_tracker.log_data_profile(
            dataset_version, 
            file_path=file_path, 
            profile=data_profile, 
            profiler_class=type(self.data_profiler).__name__
            )

    def check_data(self, data, dataset_version): 
        #run data checks
        data_report, file_path, checks_status = self.data_checker.check_data(data)

        #log data report to metadata tracker
        self.metadata_tracker.log_checks(
            dataset_version,
            file_path = file_path, 
            report = data_report, 
            checker_class = type(self.data_checker).__name__, 
            type = "data"
            )

        if checks_status == "ERROR" or checks_status == "WARN": 
            url = self.metadata_tracker.url
            self.notify("Issues found with data checks. Visit %s for more information." %url, checks_status)
        
    def compare_data(self, data, dataset_version):
        #get previous dataset version & dataframe 
        prev_dataset_version = self.metadata_tracker.get_prev_resource_version(dataset_version)
        vc_info = self.metadata_tracker.get_vc_info(prev_dataset_version)
        prev_data = self.resource_version_control.get_data(prev_dataset_version, vc_info, key = "data_csv")

        #compare current dataset version with previous dataset version
        comparison_report, file_path = self.data_profiler.compare_data(data, prev_data)

        self.metadata_tracker.log_data_comparison(
            dataset_version,
            file_path = file_path, 
            report = comparison_report, 
            profiler_class = type(self.data_profiler).__name__
            )