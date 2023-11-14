from lolpop.utils import common_utils as utils
from omegaconf import OmegaConf
from inspect import currentframe
import os
class BasePipeline: 

    __REQUIRED_CONF__ = {
        "components": [], 
        "config": []
    }
    __DEFAULT_CONF__ = {
        "config" : {}
    }

    suppress_logger = False
    suppress_notifier = False

    def __init__(self, conf={}, runner_conf={}, parent_integration_type="runner", problem_type=None,
                 pipeline_type="base_pipeline", components={}, plugin_mods=[], plugin_paths=[], 
                 skip_config_validation=False, decorators=[], *args, **kwargs):
        #set basic properties like configs
        self.name = type(self).__name__
        self.integration_type = "pipeline"
        try: 
            self.type = self.__module__.split(".")[-2]
        except: #using custom class
            self.type = self.__module__
        conf = utils.get_conf(conf)
        self.parent_integration_type = parent_integration_type
        self.pipeline_type = pipeline_type
        self.runner_conf = runner_conf
        self.problem_type = problem_type

        #resolve any variables
        conf = utils.resolve_conf_variables(conf)
        #merge into default conf
        conf = OmegaConf.create(conf)
        #merge pipeline conf into runner conf
        valid_conf = conf.copy()
        OmegaConf.update(valid_conf, "config", 
                         utils.copy_config_into(valid_conf.get("config", {}), 
                                                utils.copy_config_into(runner_conf, self.__DEFAULT_CONF__.get("config",{}))
                                                )
                        )
        #validate configuration
        if not skip_config_validation:
            valid_conf = self._validate_conf(valid_conf, components)
        self.config = utils.copy_config_into(conf, self.__DEFAULT_CONF__).get("config",{})

        #handle default components: logger, notifier, metadata_tracker
        components = utils.set_up_default_components(self, valid_conf, self.runner_conf,
                                                            plugin_mods=plugin_mods,
                                                            skip_config_validation=skip_config_validation,
                                                            components=components, 
                                                            )
        
        #handle decorators for pipeline
        decorators = decorators + utils.set_up_decorators(self, valid_conf, plugin_mods=plugin_mods, components=components)

        #set up reference to each component that is passed in from runner. 
        for component in components.keys(): 
            setattr(self, component, components.get(component))

        pipeline_conf = self.config
        pipeline_conf["pipeline_type"]=self.pipeline_type

        #handle plugins
        if len(plugin_mods) == 0: 
            if len(plugin_paths) == 0:
                plugin_paths = self._get_config("plugin_paths", [])
            file_path = None
            if hasattr(self, "__file_path__"):
                file_path = self.__file_path__
            plugin_mods = utils.get_plugin_mods(self, plugin_paths, file_path)
        self.plugin_mods = plugin_mods

        #now handle all components explicitly set for pipeline
        #note: this will override any component name inherited from the runner, which is what we want
        pipeline_components = {}
        if "components" in conf.keys(): 
            for component in conf.get("components",{}).keys(): 
                obj = utils.register_component_class(self, conf, component, pipeline_conf = pipeline_conf, 
                                                     runner_conf=runner_conf, parent_integration_type=self.integration_type,
                                                     problem_type = self.problem_type, dependent_components=components, 
                                                     plugin_mods=plugin_mods, decorators=decorators, 
                                                     skip_config_validation=skip_config_validation)
                if obj is not None: 
                    self.log("Loaded class %s into component %s" %(type(getattr(self, component)).__name__, component))
                    pipeline_components[component] = obj
                else: 
                    self.log("Unable to load class for component %s" %
                             component)

        #now update all pipeline scope components to know about the other pipeline components
        for obj in pipeline_components.values(): 
            obj._update_components(components = pipeline_components)

    def _validate_conf(self, conf, components, skip_validation=False):
        missing, total_missing = utils.validate_conf(conf, self.__REQUIRED_CONF__, components)
        if total_missing > 0: 
            #check to see if missing components are provided by runner via kwargs
            if len(missing.get("components")) > 0: 
                for component in missing.get("components"): 
                    if components.get(component, None) is not None: 
                        total_missing = total_missing - 1
            if total_missing > 0:   
                raise Exception ("Missing the following from pipeline configuration: %s" %missing)
        return conf

    def log(self, msg, level="INFO", *args, **kwargs): 
        if not self.suppress_logger: 
            self.logger.log(msg, level, process_name=self.name,
                            line_num=currentframe().f_back.f_lineno, **kwargs)

    def notify(self, msg, level="ERROR", *args, **kwargs): 
        if not self.suppress_notifier: 
            self.notifier.notify(msg, level)
            self.log("Notification Sent: %s" %msg, level)

    #helper function for lookup up config key in pipeline or runner conf
    def _get_config(self, key, default_value=None): 
        key = key.lower()
        value = utils.lower_conf(self.config).get(key, None)
        if value is None: 
            value = utils.lower_conf(self.runner_conf).get(key, default_value)
            if value is None: 
                value = os.getenv(key)
        return value 

    def _set_config(self, key, value): 
        key = key.lower()
        self.config[key]=value
