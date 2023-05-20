from omegaconf import OmegaConf
from lolpop.utils import common_utils as utils
import os 
from pathlib import Path
from inspect import currentframe
class BaseRunner: 

    __REQUIRED_CONF__ = {
        "pipelines": [], 
        "components": ["metadata_tracker"], 
        "config": []
    }
    __DEFAULT_CONF__ = {
        "config" : {}
    }

    suppress_logger = False 
    suppress_notifier = False

    def __init__(self, conf={}, problem_type = "unspecified_problem_type", plugin_paths=[], 
                 skip_config_validation=False, *args, **kwargs):
        #handle configuration 
        self.name = type(self).__name__
        conf = utils.get_conf(conf)
        conf = utils.resolve_conf_variables(conf)
        conf = utils.copy_config_into(conf, self.__DEFAULT_CONF__) 
        if not skip_config_validation:
            conf = self._validate_conf(conf)
        self.config = conf.get("config", {})
        self.problem_type = conf.get("problem_type", problem_type)

        #handle plugins
        if len(plugin_paths) == 0: 
            plugin_paths=conf.get("plugin_paths",[])
        file_path = None
        if hasattr(self, "__file_path__"): 
            file_path = self.__file_path__
        plugin_mods = utils.get_plugin_mods(self, plugin_paths, file_path)
        self.plugin_mods = plugin_mods

        #config defines all pipelines in `pipelines`
        #format is 
        ## pipelines: 
        ##   <pipeline>: <class> 
        ## components: 
        ##    <component>: <class>
        # then you need to also have a directory pipeline/component with all pipelines/components defined in subdirectories
        # later on in your yaml you need to specify configuration for the pipline via 
        ## <pipeline>: 
        ##    <key>: <value>
        # components can be defined at the runner or pipeline level and this determines the component scope.  
        # components defined at the runner level are passed down to all pipelines and components, 
        # so that they are globally acessible, whereas a component defined at the pipeline level are only accessible
        # in that pipeline and components defined at that pipeline. 
        # componenets in the right scope should know about each other but pipelines act independently (for now, at least)

        #set up logger first because we want to pass that to all children
        #we set this up separately from the other components in case you want access to the logger in the 
        #__init__ function
        logger_obj = utils.register_component_class(self, conf, "logger", default_class_name="StdOutLogger", 
                                                    runner_conf = self.config, plugin_mods=plugin_mods, 
                                                    skip_config_validation=skip_config_validation)
        if logger_obj is not None: 
            runner_components = {"logger" : logger_obj}
            self.log("Loaded class %s into component %s" %(type(self.logger).__name__, "logger"))
        else: 
            raise Exception("Unable to find logger class.", level="ERROR")

        #we also want to special handle the metadata tracker, so we'll set that up first as well and pass 
        #it to all children so they have access in __init__. 
        #it's unclear why you might not want to use a metadata tracker, 
        #but we sould consider this use case in the future 
        meta_obj = utils.register_component_class(self, conf, "metadata_tracker", runner_conf=self.config, parent_process=self.name,
                                                  problem_type=self.problem_type, dependent_components=runner_components, 
                                                  plugin_mods=plugin_mods, skip_config_validation=skip_config_validation)
        if meta_obj is not None:
            runner_components["metadata_tracker"] = meta_obj
            self.log("Loaded class %s into component %s" %(type(self.metadata_tracker).__name__, "metadata_tracker"))
        else: 
            #for local dev you may turn off metadata_tracker, so let's not strictly enforce that it exists for now
            self.log("Unable to load metadata_tracker component.")

        #build all other components
        for component in conf.components.keys(): 
            #ignore logger and metadata_tracker since we have already set those up
            if component != "logger" and component !="metadata_tracker": 
                obj = utils.register_component_class(self, conf, component, runner_conf=self.config, parent_process=self.name,
                                                     problem_type=self.problem_type, dependent_components=runner_components, 
                                                     plugin_mods=plugin_mods, skip_config_validation=skip_config_validation)
                if obj is not None: 
                    self.log("Loaded class %s into component %s" %(type(getattr(self, component)).__name__, component))
                    runner_components[component] = obj
                else: 
                    raise Exception("Unable to load class for component %s" %component)

        #now that all component classes are built, we want to update all components so that they know about each other. 
        # there is probably a more elegant way to do this
        for obj in runner_components.values(): 
            obj._update_components(components = runner_components)

        #build all pipelines 
        for pipeline in conf.pipelines.keys(): 
            utils.register_pipeline_class(self, conf, pipeline, runner_conf=self.config, parent_process=self.name,
                                          problem_type=self.problem_type, dependent_components=runner_components, 
                                          plugin_mods=plugin_mods, skip_config_validation=skip_config_validation)
            self.log("Loaded class %s into pipeline %s" %(type(getattr(self, pipeline)).__name__, pipeline))

    def _validate_conf(self, conf):
        missing, total_missing = utils.validate_conf(conf, self.__REQUIRED_CONF__, conf.get("components"))
        if total_missing>0: 
            #logger is not necessarily set up yet
            #self.logger.log("Missing the following from runner configuration: %s" %missing)
            raise Exception("Missing the following from runner configuration: %s" %missing) 
        return conf

    def log(self, msg, level="INFO", **kwargs): 
        if not self.suppress_logger: 
            self.logger.log(msg, level, process_name=self.name,
                            line_num=currentframe().f_back.f_lineno, **kwargs)

    def notify(self, msg, level="ERROR"): 
        if not self.suppress_notifier: 
            self.notifier.notify(msg, level)
            self.log("Notification Sent: %s" %msg, level)

    #helper function for lookup up config key
    def _get_config(self, key, default_value=None):
        key = key.lower()
        value = utils.lower_conf(self.config).get(key, None)
        return value
        
    def _set_config(self, key, value): 
        key = key.lower()
        self.config[key]=value