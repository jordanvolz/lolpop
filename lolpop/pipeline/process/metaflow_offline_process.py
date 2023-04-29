from lolpop.pipeline.process.abstract_process import AbstractProcess
from lolpop.utils import common_utils as utils
from metaflow import FlowSpec, step, cli, IncludeFile
import sys
import importlib
import os
from pathlib import Path

METAFLOW_CLASS = "MetaflowOfflineProcessSpec"
PLUGIN_PATHS = "plugin_paths.txt"


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class MetaflowOfflineProcess(AbstractProcess):
    __REQUIRED_CONF__ = {
        "components": ["data_transformer", "metadata_tracker", "resource_version_control", "data_profiler", "data_checker"],
        "config": []
    }

    def run(self, source_data_name, **kwargs):
        #add the parent directory to this file into the class path
        parent_dir = os.path.dirname(__file__)
        module_name = Path(__file__).stem
        sys.path.append(str(parent_dir))

        #import this file and load the metaflow class in this file
        mod = importlib.import_module(module_name)
        mod_cl = getattr(mod, METAFLOW_CLASS)

        #get all child plugin paths and write to file
        #we have to do this because we save the lolpop component as
        #part of metaflow and when it loads up it will fail if plugins
        #are used and not on the system path. This ensures that they are.
        plugin_paths = utils.get_all_plugin_paths(self)
        with open(PLUGIN_PATHS, "w") as f:
            f.write("|".join([str(x) for x in plugin_paths]))

        #load up the metaflow flow.
        flow = mod_cl(use_cli=False, lolpop_pipeline=self,
                      source=source_data_name, plugin_paths=plugin_paths, **kwargs)
        self.log("Loaded metaflow flow %s" % METAFLOW_CLASS)
        try:
            #now call the main metaflow workflow
            cli.main(flow, args=["run"], entrypoint=[sys.executable, __file__])
        except SystemExit:  # metaflow always ends by calling systemexit.
            self.log("Metaflow pipeline %s finished." % METAFLOW_CLASS)
        finally:  # remove dir from system path to be safe
            sys.path.remove(str(parent_dir))
            os.remove(PLUGIN_PATHS)

class MetaflowOfflineProcessSpec(FlowSpec):

    def __init__(self, lolpop_pipeline=None, source=None, use_cli=False, plugin_paths=None, **kwargs):
        #you need to set local attributes before calling super
        #only the first time we create the class will these parameters be provided.
        #The rest of the calls are metaflow internal calls and we do not want to reset them
        if lolpop_pipeline:
            self.lolpop_pipeline = lolpop_pipeline
        if source:
            self.source = source
        if plugin_paths:
            self.plugin_paths = plugin_paths

        #read the plugin paths from file
        with open(PLUGIN_PATHS) as f:
            plugin_paths = [Path(x) for x in f.read().split("|")]

        #load plugins. This ensures that self.lolpop_pipeline is always populated
        _ = utils.load_plugins(plugin_paths)
        
        #call init -- this kicks off the main workflow
        super().__init__(use_cli=use_cli)

    @step
    def start(self):
        self.next(self.transform_data)

    @step
    def transform_data(self):
        #transform data
        self.data = self.lolpop_pipeline.data_transformer.transform(
            self.source)

        self.next(self.track_data)

    @step
    def track_data(self):
        #create dataset version
        dataset_version = self.lolpop_pipeline.metadata_tracker.create_resource(
            self.source, type="dataset_version")
        self.dataset_version = dataset_version
        self.lolpop_pipeline.datasets_used.append(dataset_version)

        #version data
        vc_info = self.lolpop_pipeline.resource_version_control.version_data(
            dataset_version, self.data)

        #register version control metadata w/ metadata tracker
        self.lolpop_pipeline.metadata_tracker.register_vc_resource(
            dataset_version, vc_info, file_type="csv")

        self.next(self.profile_data)

    @step
    def profile_data(self):
        #profile data
        data_profile, file_path = self.lolpop_pipeline.data_profiler.profile_data(
            self.data)

        #log profile to metadata tracker
        self.lolpop_pipeline.metadata_tracker.log_data_profile(
            self.dataset_version,
            file_path=file_path,
            profile=data_profile,
            profiler_class=self.lolpop_pipeline.data_profiler.name
        )
        self.next(self.check_data)

    @step
    def check_data(self):
        #run data checks
        data_report, file_path, checks_status = self.lolpop_pipeline.data_checker.check_data(
            self.data)

        #log data report to metadata tracker
        self.lolpop_pipeline.metadata_tracker.log_checks(
            self.dataset_version,
            file_path=file_path,
            report=data_report,
            checker_class=self.lolpop_pipeline.data_checker.name,
            type="data"
        )

        if checks_status == "ERROR" or checks_status == "WARN":
            url = self.lolpop_pipeline.metadata_tracker.url
            self.lolpop_pipeline.notify(
                "Issues found with data checks. Visit %s for more information." % url, checks_status)
        self.next(self.compare_data)

    @step
    def compare_data(self):
        #get previous dataset version & dataframe
        prev_dataset_version = self.lolpop_pipeline.metadata_tracker.get_prev_resource_version(
            self.dataset_version)

        if prev_dataset_version is not None:
            vc_info = self.lolpop_pipeline.metadata_tracker.get_vc_info(
                prev_dataset_version)
            prev_data = self.lolpop_pipeline.resource_version_control.get_data(
                prev_dataset_version, vc_info)

            #compare current dataset version with previous dataset version
            comparison_report, file_path = self.lolpop_pipeline.data_profiler.compare_data(
                self.data, prev_data)

            self.lolpop_pipeline.metadata_tracker.log_data_comparison(
                self.dataset_version,
                file_path=file_path,
                report=comparison_report,
                profiler_class=self.lolpop_pipeline.data_profiler.name
            )
        else:
            self.lolpop_pipeline.log("No previous dataset version found for dataset: %s" % (
                self.lolpop_pipeline.metadata_tracker.get_resource_id(self.dataset_version)))

        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == '__main__':
    #need to use CLI here because metaflow calls back into this function to
    #execute each individual step
    MetaflowOfflineProcessSpec(use_cli=True)
