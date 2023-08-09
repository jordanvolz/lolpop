from lolpop.utils import common_utils as utils
from omegaconf import OmegaConf
from inspect import currentframe
import os
class BaseComponent: 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    __DEFAULT_CONF__ = {
        "config" : {}
    }

    suppress_logger = False
    suppress_notifier = False 

    def __init__(self, conf={}, pipeline_conf={}, runner_conf={}, parent_process=None, problem_type = None, 
                 components = {}, skip_config_validation=False, *args, **kwargs):
        #set basic properties, like name and configs
        self.name = type(self).__name__
        try: 
            self.type = self.__module__.split(".")[-2]
        except: 
            self.type = self.__module__
        self.integration_type = self.__module__.split(".")[-1]
        config = utils.get_conf(conf)
        self.pipeline_conf = pipeline_conf
        self.runner_conf = runner_conf
        self.parent_process = parent_process
        self.problem_type = problem_type

        #resolve variables
        config = utils.resolve_conf_variables(config)
        # copy config into the default config
        omega_conf = utils.copy_config_into(OmegaConf.create(config), self.__DEFAULT_CONF__)
        # set config. This ensures that we pick up any default config as well
        valid_conf = omega_conf.copy()
        # update config.config with runner and pipeline config.
        # Needs to be done in this order to keep config precedence
        OmegaConf.update(valid_conf, "config",
                         utils.copy_config_into(valid_conf.get("config", {}),
                                                utils.copy_config_into(pipeline_conf, runner_conf)
                                                )
                        )

        #Now we validate config to make sure the component has everything it needs
        if not skip_config_validation: 
            self._validate_conf(valid_conf, components)
        self.config = omega_conf.get("config", {})

        #handle default components: logger, notifier, metadata_tracker
        components = utils.set_up_default_components(self, valid_conf, self.runner_conf,
                                                     skip_config_validation=skip_config_validation,
                                                     components=components)

        #if the config looks good, then we can set all our components 
        for component in components.keys(): 
            setattr(self, component, components.get(component))
        
    def _update_components(self, components = {}, *args, **kwargs): 
        for component in components.keys(): 
            setattr(self, component, components.get(component))

    def _validate_conf(self, conf, components):
        missing, total_missing = utils.validate_conf(conf, self.__REQUIRED_CONF__, components)
        if total_missing>0: 
            #check to see if missing components are provided by runner
            if len(missing.get("components",{})) > 0: 
                for component in missing.get("components"): 
                    if components.get(component, None) is not None: 
                        total_missing = total_missing - 1
            if total_missing > 0:   
                raise Exception ("Missing the following from %s component configuration: %s" %(type(self).__name__, missing))

    def log(self, msg, level="INFO", *args, **kwargs): 
        if not self.suppress_logger:
            self.logger.log(msg, level, process_name=self.name, 
                            line_num=currentframe().f_back.f_lineno, *args, **kwargs)


    def notify(self, msg, level="ERROR", *args, **kwargs): 
        if not self.suppress_notifier: 
            self.notifier.notify(msg, level, *args, **kwargs)
            self.log("Notification Sent: %s" %msg, level)

    #helper function to lookup config key in component, pipeline or runner conf
    def _get_config(self, key, default_value=None):
        key = key.lower()
        value = utils.lower_conf(self.config).get(key, None)
        if value is None: 
            value = utils.lower_conf(self.pipeline_conf).get(key, None)
            if value is None: 
                value = utils.lower_conf(self.runner_conf).get(key, default_value)
                if value is None: 
                    value = os.getenv(key)
        return value

    def _set_config(self, key, value): 
        key = key.lower()
        self.config[key]=value
