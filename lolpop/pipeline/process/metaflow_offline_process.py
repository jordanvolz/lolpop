from lolpop.pipeline.process.base_process import BaseProcess
from lolpop.utils import common_utils as utils
from lolpop.utils import metaflow_utils as meta_utils
from metaflow import FlowSpec, step
from pathlib import Path

METAFLOW_CLASS = "MetaflowOfflineProcessSpec"
PLUGIN_PATHS = "plugin_paths.txt"


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class MetaflowOfflineProcess(BaseProcess):
    __REQUIRED_CONF__ = {
        "components": ["data_transformer", "metadata_tracker", "resource_version_control", "data_profiler", "data_checker"],
        "config": []
    }

    def run(self, source_data_name, source_data, **kwargs):
        """
        Execute the offline Metaflow flow.

        Args:
            source_data_name (str): The name of the data source.
            source_data (object): The object containing the source data.
            **kwargs: Any additional arguments to pass to the flow.

        Returns:
            None.

        Raises:
            Any exceptions raised during Metaflow execution.
        """
        #get flow class object from this file
        mod_cl = meta_utils.get_flow_class(__file__, METAFLOW_CLASS)
        
        flow = meta_utils.load_flow(mod_cl, self, PLUGIN_PATHS, source_data=source_data, source_data_name=source_data_name)
        self.log("Loaded metaflow flow %s" % METAFLOW_CLASS)

        meta_utils.run_flow(flow, "run", __file__, PLUGIN_PATHS)
        self.log("Metaflow pipeline %s finished." % METAFLOW_CLASS)

    def get_artifacts(self, artifact_keys):
        """
        Retrieve artifacts from the latest run of the pipeline.

        Args:
            artifact_keys (list): A list of artifact keys to retrieve.

        Returns:
            artifacts (dict): A dictionary containing the requested artifacts.

        Raises:
            Any exception raised during the retrieval of artifacts from the run.
        """
        #get latest run of this pipeline
        run = meta_utils.get_latest_run(METAFLOW_CLASS)

        #get requested artifacts
        artifacts = meta_utils.get_run_artifacts(run, artifact_keys, METAFLOW_CLASS)

        return artifacts
class MetaflowOfflineProcessSpec(FlowSpec):

    def __init__(self, lolpop=None, source_data=None, source_data_name=None, use_cli=False, **kwargs):
        #you need to set local attributes before calling super
        #only the first time we create the class will these parameters be provided.
        #The rest of the calls are metaflow internal calls and we do not want to reset them
        if lolpop is not None:
            self.lolpop = lolpop
        if source_data is not None:
            self.source_data = source_data
        if source_data_name is not None: 
            self.source_data_name = source_data_name

        #load plugins
        meta_utils.load_plugins(PLUGIN_PATHS)

        #call init -- this kicks off the main workflow
        super().__init__(use_cli=use_cli)

    @step
    def start(self):
        self.next(self.transform_data)

    @step
    def transform_data(self):
        #transform data
        self.data = self.lolpop.data_transformer.transform(
            self.source_data)

        self.next(self.track_data)

    @step
    def track_data(self):
        #create dataset version
        dataset_version = self.lolpop.metadata_tracker.create_resource(
            self.source_data_name, type="dataset_version")
        self.dataset_version = dataset_version
        self.lolpop.datasets_used.append(dataset_version)

        #version data
        vc_info = self.lolpop.resource_version_control.version_data(
            dataset_version, self.data)

        #register version control metadata w/ metadata tracker
        self.lolpop.metadata_tracker.register_vc_resource(
            dataset_version, vc_info, file_type="csv")

        
        self.next(self.profile_data)

    @step
    def profile_data(self):
        if (not self.lolpop.problem_type == "timeseries") or (self.source_data_name == "train_data"):
            #profile data
            data_profile, file_path = self.lolpop.data_profiler.profile_data(
                self.data)

            #log profile to metadata tracker
            self.lolpop.metadata_tracker.log_data_profile(
                self.dataset_version,
                file_path=file_path,
                profile=data_profile,
                profiler_class=self.lolpop.data_profiler.name
            )
        self.next(self.check_data)

    @step
    def check_data(self):
        if (not self.lolpop.problem_type == "timeseries") or (self.source_data_name == "train_data"):
            #run data checks
            data_report, file_path, checks_status = self.lolpop.data_checker.check_data(
                self.data)

            #log data report to metadata tracker
            self.lolpop.metadata_tracker.log_checks(
                self.dataset_version,
                file_path=file_path,
                report=data_report,
                checker_class=self.lolpop.data_checker.name,
                type="data"
            )

            if checks_status == "ERROR" or checks_status == "WARN":
                url = self.lolpop.metadata_tracker.url
                self.lolpop.notify(
                    "Issues found with data checks. Visit %s for more information." % url, checks_status)
                
        self.next(self.compare_data)

    @step
    def compare_data(self):
        if not (self.lolpop.problem_type == "timeseries"):
            #get previous dataset version & dataframe
            prev_dataset_version = self.lolpop.metadata_tracker.get_prev_resource_version(
                self.dataset_version)

            if prev_dataset_version is not None:
                vc_info = self.lolpop.metadata_tracker.get_vc_info(
                    prev_dataset_version)
                prev_data = self.lolpop.resource_version_control.get_data(
                    prev_dataset_version, vc_info)

                #compare current dataset version with previous dataset version
                comparison_report, file_path = self.lolpop.data_profiler.compare_data(
                    self.data, prev_data)

                self.lolpop.metadata_tracker.log_data_comparison(
                    self.dataset_version,
                    file_path=file_path,
                    report=comparison_report,
                    profiler_class=self.lolpop.data_profiler.name
                )
            else:
                self.lolpop.log("No previous dataset version found for dataset: %s" % (
                    self.lolpop.metadata_tracker.get_resource_id(self.dataset_version)))

        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == '__main__':
    #need to use CLI here because metaflow calls back into this function to
    #execute each individual step
    MetaflowOfflineProcessSpec(use_cli=True)
