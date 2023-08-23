import subprocess 
import os 
import sys
from importlib import import_module, util as import_util 
from git import Repo
from omegaconf import OmegaConf, dictconfig
from datetime import datetime
from functools import wraps 
import pandas as pd 
from pathlib import Path 
import time

#
##should decide if these things go into the common_utils class or just the abstract classes. 
#

#shell command wrapper
def execute_cmd(cmd, logger=None):
    if logger: 
        logger.log("Executing command: `%s`" %(" ".join(cmd)))
    p = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=False)
    return (p.stdout, p.returncode)

# pulls keys out of config or gets from env variable
# i.e. either handle secret manager before getting here and pass in 
# or populate via env vars
def load_config(config_keys, conf): 
    config = {}
    for key in config_keys: 
        if key in conf.keys():
            config[key]=conf[key]
        elif key.lower() in conf.keys(): #handle cases where we're looking for env var but it's overridden in conf w/ lowercase 
            config[key] = conf[key.lower()]
        else: 
            config[key] = os.getenv(key)
    return config

#comits a single file to git
def git_commit_file(file_path, repo_path=None, msg="Commiting file from lolpop", push=False, path_from_root=None, logger=None):
    repo = Repo(repo_path,search_parent_directories=True)
    if path_from_root is not None: 
        file_path = "%s/%s" %(path_from_root, file_path)
    repo.index.add(file_path)
    hexsha = repo.index.commit(msg).hexsha

    if push: 
        origin = repo.remotes[0]
        result = origin.push()
        if logger: 
            logger.log("Committed and pushed file %s. Result: %s" %(file_path, result[0].summary))

    return hexsha

def load_plugins(plugin_paths=[]):
    plugins = []
    for dir in plugin_paths:
        if dir.exists():
            plugin = load_plugin(dir)
            plugins.append(plugin)
    return plugins

def load_plugin(plugin_path, obj=None): 
    #get plugin directory path and name
    plugin_path = plugin_path.resolve() #in case absolute path is not passed in in yaml
    if plugin_path.is_dir(): 
        plugin_dir = str(plugin_path)
        plugin_name = plugin_path.name
    elif plugin_path.is_file():
        plugin_dir = str(plugin_path.parent)
        plugin_name = plugin_path.stem
    else: 
        raise Exception("Invalid plugin path: %s. Path is not a file nor a directory." %plugin_path)
    #append directory to sys path
    if plugin_dir: 
        sys.path.append(plugin_dir)
    #import module
    mod = None
    #there's only a module to load if we're passed a file 
    if plugin_path.is_file(): 
        if plugin_name: 
            mod = import_module(plugin_name)
    #if object passed in, append plugin dir to plugin_paths config
    #this is mainly used for local data transformer component
    if obj: 
        plugin_paths = obj._get_config("plugin_paths",[]) 
        plugin_paths.append(plugin_dir)
        obj._set_config("plugin_paths", plugin_paths)
    return mod

#load class object
def load_class_obj(class_name, class_type="component", parent="lolpop"): 
    try: 
        module = import_module("%s.%s" %(parent, class_type))
        cl = getattr(module, class_name)
    except: 
        module = import_module(parent)
        cl = getattr(module, class_name)
    return cl

def load_class(class_name, class_type="component", plugin_mods = [], self_obj=None): 
    try:
        cl = load_class_obj(class_name, class_type)
    except: 
        try: 
            if self_obj: 
                self_obj.log("Unable to find class %s in build-in resources. Searching extensions..." %class_name)
            cl = load_class_obj(class_name, class_type="extension")
            if self_obj:
                self_obj.log("Found class %s in extensions!" %class_name)
        except: 
            if self_obj:
                self_obj.log(
                    "Unable to find class %s in extensions. Searching plugins modules in %s..." %(class_name, str(plugin_mods)))
            cl = load_class_from_plugin(class_name, plugin_mods, class_type)
            if cl is not None: 
                if self_obj: 
                    self_obj.log("Found class %s in plugins!" % class_name)
            else: 
                if self_obj:
                    self_obj.log("Unable to find class %s in plugins!" %class_name)
    return cl 

#load class object from plugins
def load_class_from_plugin(class_name, plugin_mods, class_type="component"):
    #try to load from each plugin
    cl = None 
    for plugin in plugin_mods: 
        try: 
            cl = load_class_obj(class_name, class_type=class_type, parent=plugin)
            break 
        except Exception as e: 
            #if multiple plugins are used, the one we are looking for will not be in most of them, so just ignore any errors
            continue 
    return cl

#loads a module from a file
def load_module_from_file(file_path): 
    spec = import_util.spec_from_file_location(file_path.stem, file_path)
    mod = import_util.module_from_spec(spec)
    sys.modules[spec.name]=mod #need to do this to properly register module
    spec.loader.exec_module(mod)
    return mod 

#register component class as an attribute of the provided object
def register_component_class(self_obj, conf, component_type, default_class_name=None, 
                             pipeline_conf = {}, runner_conf = {}, parent_process = "runner", 
                             problem_type = None, dependent_components = {}, plugin_mods=[], *args, **kwargs): 
    obj = None
    component_class_name = conf.get("components",{}).get(component_type, default_class_name)
    if component_class_name is not None:
        cl = load_class(component_class_name) 
        if cl is not None: 
            obj = cl(conf=conf.get(component_type, {}), pipeline_conf=pipeline_conf, runner_conf=runner_conf,
                     parent_process=parent_process, problem_type=problem_type, components=dependent_components, *args, **kwargs)
            setattr(self_obj, component_type, obj)
    return obj 

#registers pipeline as an attribute of the provided object
def register_pipeline_class(self_obj, conf, pipeline_type, default_class_name=None, runner_conf = {}, 
                            parent_process = "runner", problem_type = None, dependent_components = {}, 
                            plugin_mods=[], *args, **kwargs): 
    obj = None 
    pipeline_class_name = conf.get("pipelines",{}).get(pipeline_type, default_class_name)
    if pipeline_class_name is not None: 
        cl = load_class(pipeline_class_name, class_type="pipeline")
        if cl is not None: 
            obj = cl(conf=conf.get(pipeline_type, {}), runner_conf=runner_conf, parent_process=parent_process,
                     problem_type=problem_type, components=dependent_components, plugin_mods=plugin_mods, *args, **kwargs)
            setattr(self_obj, pipeline_type, obj)
    return obj

def lower_conf(conf): 
    return {k.lower():v for k,v in conf.items()}
    
#Need to revisit. Seems like this is not actually merging on update, it's reassigning. 
#As a result, some default conf can get lost
def copy_config_into(conf, default_conf): 
    #have to use omegaconf so types match
    default_copy = OmegaConf.create(default_conf.copy())
    updated_conf = OmegaConf.merge(default_copy, conf)
    return updated_conf

#validates configuration with the required conf specified
def validate_conf(config, required_conf, components_objs={}):
    conf = config.copy()
    #convert componenets_obj dict into primitives
    components = OmegaConf.create({k:type(v).__name__ for k,v in components_objs.items()})
    #updates conf.components with components. 
    #we want local config values to overwrite glboals, so we do a two step update
    if conf.get("components", None) is None: 
        conf["components"]=components
    else: 
        components.update(conf.get("components",{}))
        conf.get("components",{}).update(components)

    missing = {}
    total_missing = 0
    if required_conf is not None: 
        if conf is None: 
            conf = {}
        #map everything to lowercase keys to avoid capitalization mismatch
        lconf = lower_conf(conf)
        lrequired_conf = lower_conf(required_conf)
        for k,v in lrequired_conf.items(): 
            missing_k = []
            for val in v: 
                #value can be of form "key|values" which specifies the value(s) allowed
                #this is mainly used to specify the classes supported
                #i.e. something like "MetadataTracker|MLFlowMetadataTracker"
                if "|" in val: 
                    val_arr = val.split("|")
                    val_key = val_arr[0]
                    val_value = val_arr[1].split(",")
                else: 
                    val_key = val
                    val_value = None
                #check if key,value exist in config
                if lconf.get(k,{}).get(val_key.lower(),None) is None: 
                    #if not provided in config, check environment variables 
                    if os.getenv(val_key.upper(),None) is None: 
                        missing_k.append(val) 
                elif val_value is not None: 
                    if lconf.get(k,{}).get(val_key.lower()) not in val_value: 
                        missing_k.append(val)
            missing[k] = missing_k
        for v in missing.values(): 
            total_missing = total_missing + len(v)
    return missing, total_missing

#replaces variable values with their actual values. 
#conf allows pointing to other variable via $node1.node2.node3, etc...
def resolve_conf_variables(conf, main_conf=None):
    if main_conf is None: #need to always have the full conf lineage because variables can pont to arbitrary nodes
        main_conf = conf
    if conf is not None and len(conf) > 0: 
        for k,v in conf.items(): 
            if isinstance(v, dictconfig.DictConfig):
                OmegaConf.update(conf, k, resolve_conf_variables(v, main_conf)) 
            elif isinstance(v, str): 
                if v[0] == "$": 
                    resolved_value = get_conf_value(v[1:], main_conf)
                    if resolved_value: 
                        OmegaConf.update(conf,k, resolved_value)
                    else: 
                        raise Exception("Unable to resolve configuration value: %s" %v)
    return conf

# returns configuration from conf object (file location or python dict)
def get_conf(conf_obj): 
    if isinstance(conf_obj, str) or isinstance(conf_obj, Path):
        conf = OmegaConf.load(conf_obj)
    elif type(conf_obj) is dict: 
        conf = OmegaConf.create(conf_obj)
    elif isinstance(conf_obj, dictconfig.DictConfig):
        conf = conf_obj
    else: 
        raise Exception("Invalid configuration. Configuration must be a file or a a dict.")
    
    return conf 

#returns node value in conf specified by var in the form 'node1.node2.node3...'
def get_conf_value(var, conf): 
    var_arr = var.split(".")
    out = conf
    try: 
        for i in var_arr: 
            out = out.get(i)
    except: 
        out = None 
    return out 

def get_plugin_mods(self_obj, plugin_paths=[], file_path=None):
    # if no plugin_dir is provided, then try to use the parent directory.
    # if the parent directory is lolpop, then it is a built-in runner and we can ignore
    if file_path is not None:
        #directory should be something like <module_name>/<runner>/<runner_type>/<runner_class>.py
        plugin_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.realpath(file_path))))
        plugin_paths.append(plugin_dir)

    plugin_paths = [Path(dir) for dir in plugin_paths if dir != "lolpop"]

    #load up all plugin modules
    plugins = load_plugins(plugin_paths)
    plugin_mods = []
    for plugin in plugins: 
        if plugin is not None: 
            plugin_mods.append(plugin.__name__)
    
    return plugin_mods

#for a given lolpop object, get all plugin paths in children
def get_all_plugin_paths(obj):
    children = [x for x in dir(obj) if not x.startswith("_")]
    plugin_paths=[]

    for child in children: 
        child_obj = getattr(obj, child)
        if hasattr(child_obj, "_get_config"): 
            paths = child_obj._get_config("plugin_paths", None)
            if paths is not None: 
                plugin_paths = plugin_paths + paths
    
    plugin_paths = [Path(path) for path in set(plugin_paths)]

    return plugin_paths

#wraps logging calls around function execution
def log_execution(level="DEBUG", start_msg = None, end_msg = None, timeit=True):
    def log_decorator(func):
        @wraps(func)
        def wrapper(obj, *args, **kwargs):
            start = start_msg
            end = end_msg
            if not start: 
                start = "Starting execution of %s" %(func.__name__)
            if not end: 
                end = "Finished execution of %s" %(func.__name__)
            obj.log(start, level)
            obj.log("args: %s, kwargs: %s" %(args, kwargs), "TRACE")
            start_time = time.process_time()
            result = func(obj, *args, **kwargs)
            end_time = time.process_time()
            if timeit: 
                end = end + ". Completed in %s seconds." %(str(end_time - start_time))
            obj.log(end, level)
            return result
        return wrapper
    return log_decorator

#wraps function around error handling
def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            #prevent unnecessary nesting
            if str(e).startswith("An error occurred:"): 
                raise e
            else: 
                raise Exception(f"An error occurred: {e}")
    return wrapper

# decorate all public methods in a class with decorator
# should only be applied to class definition
# decorators can be a single decorator or list of decorators that will be applied in reverse order
# i.e. the first decorator in the list would be the topmost decorator if listed out
# (this seems like the intuitive thing to do)
def decorate_all_methods(decorators):
    def decorate(cls):
        decorator_list = decorators
        if not isinstance(decorator_list, list):
            decorator_list=[decorator_list]
        for attr in dir(cls):
            if callable(getattr(cls, attr)) and not attr.startswith("_") and attr !="log" and attr !="notify":
                func = getattr(cls,attr)
                for decorator in decorator_list[::-1]: 
                    func = decorator(func)
                setattr(cls, attr, func)
        return cls
    return decorate

#compares two dataframes and tries to convert columns so that match types if they don't otherwise
def compare_data_schemas(obj, data, prev_data):
    #check to see if schemas are equal
    ok = True 
    if not data.equals(prev_data): 
        #if they are not equal, try to set schemas to be the same. 
        ok = False
        try: 
            data = convert_col_types(data, prev_data)
            ok = True
        except Exception as e: 
            obj.notify("Data Comparison failed. New and old dataframes do not have compatible column types. Error: %s" %str(e), "ERROR")
            raise 
    return data, prev_data, ok

def convert_col_types(data, prev_data):
    df_a = data.copy()
    df_b = prev_data.copy()
    for col in df_a.columns:
        if col in df_b.columns: #if col is net new, we can skip
            if df_a[col].dtype != df_b[col].dtype:
                df_a[col] = df_a[col].astype(df_b[col].dtype)
    return df_a

#True = higher is better (descending)
def get_metric_direction(perf_metric): 
    reverse = True 
    if perf_metric in ["mse", "rmse", "mae", "mdae", "mape", "smape", "rmsle", "msle"]: 
        reverse = False 
    return reverse

#labels should be something like data["y_train"].unique()
def get_multiclass(labels): 
    classification_type = "binary"
    num_classes = len(labels)
    if num_classes > 2: 
        classification_type = "multiclass"

    return classification_type


def create_df_from_file(source_file, engine="pyarrow", **kwargs): 
    _, source_file_type = str(source_file).split("/")[-1].split(".")
    data = pd.DataFrame()
    if source_file_type == "csv":
        data = pd.read_csv(source_file, engine=engine, **kwargs)
    elif source_file_type in ["parquet", "pq"]:
        data = pd.read_parquet(source_file, engine=engine, **kwargs)
    else:
        raise Exception("Unsupported file type: %s" % source_file_type)
    
    return data

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


#generates a test plan from a configuration file
def generate_test_plan(config, test_plan={}, parent=None, logger=None, test_recorder=None): 
    config = get_conf(config)
    components = config.pop("components", {})
    #set up logger
    if logger is None: 
        logger_cl = load_class(components.get("test_logger",None))
        if logger_cl is not None: 
            logger_conf = config.pop("test_logger",{})
            logger = logger_cl(conf=logger_conf)

    #set up test_recorder
    if test_recorder is None:
        test_recorder_cl = load_class(components.get("test_recorder", "LocalTestRecorder"))
        if test_recorder_cl is not None:
            test_recorder_conf = config.pop("test_recorder", {})
            test_recorder = test_recorder_cl(conf=test_recorder_conf)

    #extract tests
    test_plan = extract_tests(config, test_plan, parent)
    
    return test_plan, logger, test_recorder


def extract_tests(config, test_plan={}, parent=None):
    config = get_conf(config)

    #extract tests
    test_list = config.pop("tests", {})
    for method in test_list:
        key = method
        if parent is not None:
            key = "%s.%s" % (parent, key)
        test_plan[key] = test_list[method]

    #anything else should be dependents + tests
    for resource in config.keys():
        key = resource
        if parent is not None:
            key = "%s.%s" % (parent, key)
        test_plan = extract_tests(config[resource], test_plan=test_plan,
                                          parent=key)
        
    return test_plan

#apply test plan to the given object
#this replaces the specified function with a wrapper that now includes 
# the pre- and post-hooks defined in the testing config
def apply_test_plan(runner, test_plan, test_recorder, test_logger=None): 

    # if no specific test logger is provided, just use the runner's log method
    if test_logger is None: 
        test_logger = runner

    for method,tests in test_plan.items(): 
        fn, obj = get_method(runner, method)
        prehooks = load_hooks(tests.get("pre-hooks"))
        posthooks = load_hooks(tests.get("post-hooks"))

        if len(prehooks) > 0 or len(posthooks) > 0: 
            runner = set_method(runner, method, test_plan_decorator(
                obj, test_logger, test_recorder, prehooks, posthooks)(fn))
            
    return runner

#load hooks from file. 
# Note: the "test" function in the hook file is the entry point
def load_hooks(hook_list): 
    hook_list_out = []
    if hook_list is not None: 
        hook_list_out = [
            (Path(x.get("hook_file")).stem, 
             getattr(load_plugin(Path(x.get("hook_file"))), x.get("hook_method","test")),
             x.get("hook_on_error", "continue").lower()) 
             for x in hook_list
        ]
    return hook_list_out

#retrieves the method on a runner path. Here 'method' is dot notation i.e. "runner.pipeline.component.method"
def get_method(obj, method):
    method_arr = method.split(".")
    out = obj, None
    try: 
        for i in method_arr:
            parent = obj
            obj = getattr(obj, i)
        out = obj, parent
    except: 
        out = None, None 
    return out 

#sets the method for the object to the specified function
def set_method(obj, method, fn):
    method_arr = method.split(".")

    if len(method_arr) == 1: 
        setattr(obj, method_arr[0], fn)
    else: 
        setattr(obj, method_arr[0], 
                set_method(getattr(obj, method_arr[0]),".".join(method_arr[1:]),fn))
        
    return obj 

#decorator used with a test plan to apply pre- and post-hooks to a function 
def test_plan_decorator(obj, logger, recorder, prehooks, posthooks, level="DEBUG"):
    def test_decorator(func): 
        @wraps(func)
        def wrapper(*args, **kwargs):
            for prehook in prehooks:
                obj.log("Running pre-hook %s.%s" %(prehook[0], prehook[1].__name__), level)
                try: 
                    passed = prehook[1](obj, *args, **kwargs)
                    msg_out = None
                    if isinstance(passed, tuple):
                        msg_out = passed[1]
                        passed = passed[0]
                    recorder.record_test(obj, func, prehook[0], prehook[1], passed, msg_out)
                    if passed: 
                        logger.log("Pre-hook %s.%s passed." %
                                   (prehook[0], prehook[1].__name__), "INFO")
                    else: 
                        logger.log("Pre-hook %s.%s failed" %
                                   (prehook[0], prehook[1].__name__), "WARN")
                    if msg_out is not None: 
                        logger.log("Pre-hook message: %s" %msg_out)
                    obj.log("Pre-hook %s.%s finished." %(prehook[0], prehook[1].__name__), level)
                except Exception as e: 
                    logger.log("Error occured when running pre-hook %s.%s: %s" % (prehook[0], prehook[1].__name__, str(e)))
                
                
            result = func(*args, **kwargs)
            
            for posthook in posthooks:
                obj.log("Running post-hook %s.%s" %
                        (posthook[0], posthook[1].__name__), level)
                try: 
                    passed = posthook[1](obj, result, *args, **kwargs)
                    msg_out = None
                    if isinstance(passed, tuple): 
                        msg_out = passed[1] 
                        passed = passed[0]
                    recorder.record_test(obj, func, posthook[0], posthook[1], passed, msg_out)
                    if passed:
                        logger.log("Post-hook %s.%s passed." %
                                   (posthook[0], posthook[1].__name__), "INFO")
                    else:
                        logger.log("Post-hook %s.%s failed" %
                                   (posthook[0], posthook[1].__name__), "WARN")
                    if msg_out is not None:
                        logger.log("Pre-hook message: %s" % msg_out)
                    obj.log("Post-hook %s.%s finished." %
                            (posthook[0], posthook[1].__name__), level)
                except Exception as e:
                    logger.log(
                        "Error occured when running post-hook %s.%s: %s" % (posthook[0], posthook[1].__name__, str(e)))
            return result
        return wrapper
    return test_decorator


def set_up_default_components(obj, conf, runner_conf,
                              plugin_mods=[],
                              skip_config_validation=False,
                              components={}):
    
    #these are the defaults, so if you're explicitly building one, skip this to avoid
    #recursion error 
    if obj.type != "logger" and obj.type != "notifier" and obj.type !="metadata_tracker":
        #set up logger first because we want to pass that to all children
        #we set this up separately from the other components in case you want access to the logger in the
        #__init__ function
        if "logger" not in components.keys(): #you were passed a logger from somewhere else, skip
            logger_obj = register_component_class(obj, conf, "logger", default_class_name="StdOutLogger",
                                                runner_conf=runner_conf, parent_process = obj.name, 
                                                plugin_mods=plugin_mods, skip_config_validation=skip_config_validation,
                                                )
            if logger_obj is not None:
                components["logger"] = logger_obj
                obj.log("Loaded class %s into component %s" %(obj.logger.name, "logger"))
            else:
                raise Exception("Unable to find logger class.")
        else: 
            setattr(obj, "logger", components["logger"])

        if "notifier" not in components.keys():#you were passed a notifier from somewhere else, skip
            notifier_obj = register_component_class(obj, conf, "notifier", default_class_name = "StdOutNotifier", 
                                                runner_conf=runner_conf, parent_process=obj.name,
                                                problem_type=obj.problem_type, dependent_components=components,
                                                plugin_mods=plugin_mods, skip_config_validation=skip_config_validation)
            if notifier_obj is not None:
                components["notifier"] = notifier_obj
                obj.log("Loaded class %s into component %s" %
                            (obj.notifier.name, "notifier"))
            else:
                obj.log("Unable to load notifier component.")
        else:
            setattr(obj, "notifier", components["notifier"])

        #we also want to special handle the metadata tracker, so we'll set that up first as well and pass
        #it to all children so they have access in __init__.
        #it's unclear why you might not want to use a metadata tracker,
        #but we sould consider this use case in the future
        if "metadata_tracker" not in components.keys() and obj.type !="metadata_tracker": #you were passed a metadata_tracker from somewhere else, skip
            meta_obj = register_component_class(obj, conf, "metadata_tracker", runner_conf=runner_conf, parent_process=obj.name,
                                                        problem_type=obj.problem_type, dependent_components=components,
                                                        plugin_mods=plugin_mods, skip_config_validation=skip_config_validation)
            if meta_obj is not None:
                components["metadata_tracker"] = meta_obj
                obj.log("Loaded class %s into component %s" %
                            (obj.metadata_tracker.name, "metadata_tracker"))
            else:
                #for local dev you may turn off metadata_tracker, so let's not strictly enforce that it exists for now
                obj.log("Unable to load metadata_tracker component.")
        else:
            setattr(obj, "metadata_tracker", components["metadata_tracker"])

    return components
