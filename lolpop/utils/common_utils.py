import subprocess 
import os 
from importlib import import_module
from git import Repo
from omegaconf import OmegaConf, dictconfig
from datetime import datetime
from functools import wraps 

#
##should decide if these things go into the common_utils class or just the abstract classes. 
#

#shell command wrapper
def execute_cmd(cmd, print_it=False):
	popen = subprocess.Popen([cmd], stdout=subprocess.PIPE, universal_newlines=True, shell=True)
	output = popen.stdout.read()
	exit_code = popen.wait()
	if print_it:
		print(output)
		#print("exit code: %s" %exit_code)
	return (output,exit_code)

# pulls keys out of config or gets form env variable
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
def git_commit_file(file_path, repo_path=None, msg="Commiting file from mlops-jumpstart"):
    repo = Repo(repo_path)
    repo.index.add(file_path)
    hexsha = repo.index.commit(msg).hexsha

    origin = repo.remotes[0]
    origin.push

    return hexsha

#get the id from the fully qualified name 
#it's odd that this lives in common_utils, but it's currently needed
#while wildcard loookup doesn't work in Continual. When that is fixed we shouldn't need it anymore. 
#def truncate_id(id): 
#    if "/" in id: 
#        id = id.split("/")[-1] #get the last piece, i.e. it's a continual name
#    return id 

#load class object
def load_class(class_name, class_type="component"): 
    module = import_module("lolpop.%s" %class_type)
    cl = getattr(module, class_name)
    return cl

#register component class as an attribute of the provided object
def register_component_class(self_obj, conf, component_type, default_class_name=None, pipeline_conf = {}, runner_conf = {}, parent_process = "runner", problem_type = None, dependent_components = None): 
    obj = None
    component_class_name = conf.components.get(component_type, default_class_name)
    if component_class_name is not None:
        cl = load_class(component_class_name) 
        obj = cl(conf.get(component_type,{}), pipeline_conf, runner_conf, parent_process = parent_process, problem_type=problem_type, components = dependent_components) 
        setattr(self_obj, component_type, obj)
    return obj 

#registers pipeline as an attribute of the provided object
def register_pipeline_class(self_obj, conf, pipeline_type, default_class_name=None, runner_conf = {}, parent_process = "runner", problem_type = None, dependent_components = None): 
    obj = None 
    pipeline_class_name = conf.pipelines.get(pipeline_type, default_class_name)
    if pipeline_class_name is not None: 
        cl = load_class(pipeline_class_name, class_type="pipeline")
        obj = cl(conf.get(pipeline_type,{}), runner_conf, parent_process = parent_process, problem_type = problem_type, components = dependent_components)
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
                #i.e. something like "MetadataTracker|ContinualMetadataTracker"
                if "|" in val: 
                    val_arr = val.split("|")
                    val_key = val_arr[0]
                    val_value = val_arr[1].split(",")
                else: 
                    val_key = val
                    val_value = None
                if conf.get(k,{}).get(val_key.lower(),None) is None: 
                    missing_k.append(val) 
                elif val_value is not None: 
                    if conf.get(k,{}).get(val_key.lower()) not in val_value: 
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
    if conf is not None: 
        for k,v in conf.items(): 
            if isinstance(v, dictconfig.DictConfig):
                OmegaConf.update(conf, k, resolve_conf_variables(v, main_conf)) 
                #conf[k] = resolve_conf_variables(v, main_conf)
            elif isinstance(v, str): 
                if v[0] == "$": 
                    OmegaConf.update(conf,k, get_conf_value(v[1:], main_conf))
                    #conf[k] = get_conf_value(v[1:], main_conf)
    return conf

#returns node value in conf specified by var in the form 'node1.node2.node3...'
def get_conf_value(var, conf): 
    var_arr = var.split(".")
    for i in var_arr: 
        conf = conf.get(i)
    return conf 

def log(obj, msg, level): 
    current_time = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S.%f")
    msg = "%s [%s] <%s> ::: %s " %(current_time, level, obj.name, msg)
    obj.logger.log(msg, level)

#wraps logging calls around function execution
def log_execution(level="INFO", start_msg = None, end_msg = None):
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
            result = func(obj, *args, **kwargs)
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
    return data, prev_data, True

def convert_col_types(data, prev_data):
    df_a = data.copy()
    df_b = prev_data.copy()
    for col in df_a.columns:
        if col in df_b.columns: #if col is net new, we can skip
            if df_a[col].dtype != df_b[col].dtype:
                df_a[col] = df_a[col].astype(df_b[col].dtype)
    return df_a

#True = lower is better
def get_metric_direction(perf_metric): 
    reverse = False 
    if perf_metric in ["mse", "rmse", "mae", "mape", "smape"]: 
        reverse = True 
    return reverse

#labels should be something like data["y_train"].unique()
def get_multiclass(labels): 
    classification_type = "binary"
    num_classes = len(labels)
    if num_classes > 2: 
        classification_type = "multiclass"

    return classification_type