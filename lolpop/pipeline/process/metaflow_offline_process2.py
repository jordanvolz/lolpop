from lolpop.pipeline.process.abstract_process import AbstractProcess
from lolpop.utils import common_utils as utils
from metaflow import FlowSpec, step, cli , IncludeFile
import sys
import importlib
import os 
from pathlib import Path 

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class MetaflowOfflineProcess2(AbstractProcess):
    __REQUIRED_CONF__ = {
        "components": ["data_transformer", "metadata_tracker", "resource_version_control", "data_profiler", "data_checker"], 
        "config": []
    }

    def run(self, source_data_name, **kwargs): 
        #metaflow_pipeline = MetaflowOfflineProcessSpec(lolpop_pipeline=self)
        #return metaflow_pipeline.transform_data(source_data_name)
        parent_dir = os.path.dirname(__file__)
        module_name = Path(__file__).stem
        sys.path.append(str(parent_dir))
        mod = importlib.import_module(module_name)
        mod_cl = getattr(mod, "MetaflowOfflineProcessSpec2")
        plugin_paths = utils.get_all_plugin_paths(self)

        with open("/tmp/artifacts/plugin_paths.txt", "w") as f: 
            f.write("|".join([str(x) for x in plugin_paths]))
            
        flow = mod_cl(use_cli=False, lolpop_pipeline=self,
                      source=source_data_name, plugin_paths=plugin_paths,**kwargs)
        print("+ loaded module")
        try: 
            print(sys.executable)
            print(__file__)
            print("+ calling cli.main!")
            cli.main(flow, args=["run"], entrypoint=[sys.executable, __file__])
        except: 
            print("Caught SystemExit!")
            #remove dir from system path to be safe
            sys.path.remove(str(parent_dir))

class MetaflowOfflineProcessSpec2(FlowSpec):

    def __init__(self, lolpop_pipeline=None, source=None, use_cli = False, plugin_paths = None, **kwargs):
        #you need to set local attributes before calling super
        print("+ printing dir(self) in init")
        print(str(dir(self)))
        #if hasattr(self, "input"):
        #    print("+ input: " + str(self.input))
        if lolpop_pipeline: 
            self.lolpop_pipeline = lolpop_pipeline
        if source: 
            self.source = source
        if plugin_paths: 
            self.plugin_paths = plugin_paths 
        with open("/tmp/artifacts/plugin_paths.txt") as f: 
            plugin_paths = [Path(x) for x in f.read().split("|")]
        print("+ plugin_paths from file: " + str(plugin_paths))
        _ = utils.load_plugins(plugin_paths)
        print("+ class check in lolpop: " + str(self.__class__))
        #self.__class__ = "__main__" + str(self.__class__).split(".")[-1]
        print("+ entering super init")
        super().__init__(use_cli=use_cli)
        print("+ finished super init")

    @step
    def start(self):
        print("+ starting next!")
        print("+ printing dir(self) in start")
        print(str(dir(self)))
        #if hasattr(self, "plugin_paths"):
        #    print("+ plugin_paths: " + str(self.plugin_paths))
        #    _ = utils.load_plugins(self.plugin_paths)
        if (hasattr(self, "source")):
            print("+ has source: " + str(self.source))
        if hasattr(self, "input"):
            print("+ input: " + str(self.input))
        if hasattr(self, "lolpop_pipeline"): 
            print("+ has lolpop obj: " + str(self.lolpop_pipeline))
        self.start_test = 1 
        self.next(self.transform_data)

    @step
    def transform_data(self):
        print("+ starting transform_data!")
        if hasattr(self, "input"):
            print("+ inputs: " + str(self.input))
        if (hasattr(self, "source")):
            print("+ has source: " + str(self.source))
        if hasattr(self, "lolpop_pipeline"):
            print("+ has lolpop obj: " + str(self.lolpop_pipeline))
        if hasattr(self, "start_test"):
            print("+ has start_test: " + str(self.start_test))
        ##get source data
        #data = self.data_connector.get_data(source_data_name)

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
        print("+ dataset_version: " + str(dataset_version))
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
        print("End")


if __name__ == '__main__':
    #need to use CLI here because metaflow calls back into this function to 
    #execute each individual step
    MetaflowOfflineProcessSpec2(use_cli=True)
