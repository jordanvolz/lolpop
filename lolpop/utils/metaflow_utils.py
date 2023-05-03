import sys
import importlib
import os
from pathlib import Path
from lolpop.utils import common_utils as utils
from metaflow import cli, Flow

def get_flow_class(flow_file_path, flow_class):
    #add the parent directory of this file into the classpath
    parent_dir = os.path.dirname(flow_file_path)
    module_name = Path(flow_file_path).stem
    sys.path.append(str(parent_dir))

    #import this file and load the metaflow class in this file
    mod = importlib.import_module(module_name)
    mod_cl = getattr(mod, flow_class)

    return mod_cl 

def load_flow(mod_cl, self_obj, plugin_paths_file, **kwargs):

    #get all child plugin paths and write to file
    #we have to do this because we save the lolpop component as
    #part of metaflow and when it loads up it will fail if plugins
    #are used and not on the system path. This ensures that they are.
    plugin_paths = utils.get_all_plugin_paths(self_obj)
    with open(plugin_paths_file, "w") as f:
        f.write("|".join([str(x) for x in plugin_paths]))

    #load up the metaflow flow.
    flow = mod_cl(use_cli=False, lolpop=self_obj, **kwargs)

    return flow

def run_flow(flow, command, flow_file_path, plugin_paths_file):
    try:
        #now call the main metaflow workflow
        cli.main(flow, args=[command], entrypoint=[sys.executable, flow_file_path])
    except SystemExit:  # metaflow always ends by calling systemexit. To avoid exiting the program, catch it and pass
        pass 
    finally:  
        # remove dir from system path to be safe
        sys.path.remove(str(os.path.dirname(flow_file_path)))
        os.remove(plugin_paths_file)


def get_latest_run(flow_class):
    flow = Flow(flow_class)
    run = flow.latest_run

    return run 

def get_run_artifacts(run, keys, flow_class): 
    if run.successful:
        artifacts = run.data._artifacts
        artifacts_out = [artifacts.get(x) for x in keys]
        return [x.data for x in artifacts_out if x is not None]
    else:
        raise Exception("Metaflow run %s for flow %s failed. Unable to retrieve artifacts." % (run.id, flow_class))


def load_plugins(plugin_paths_file):
    #read the plugin paths from file
    plugin_paths = []
    with open(plugin_paths_file) as f:
        plugin_paths = [Path(x) for x in f.read().split("|") if len(x)>0]

    #load plugins. This ensures that self.lolpop is always populated
    if len(plugin_paths) > 0: 
        _ = utils.load_plugins(plugin_paths)
