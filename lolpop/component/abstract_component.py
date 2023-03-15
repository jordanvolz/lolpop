from lolpop.utils import common_utils as utils
from omegaconf import OmegaConf
class AbstractComponent: 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    __DEFAULT_CONF__ = {
        "config" : {}
    }

    def __init__(self, config={}, pipeline_conf={}, runner_conf={}, parent_process=None, problem_type = None, components = {}, *args, **kwargs):
        #set basic properties, like name and configs
        self.name = type(self).__name__
        self.config = config.get("config", {})
        self.pipeline_conf = pipeline_conf
        self.runner_conf = runner_conf
        self.parent_process = parent_process
        self.problem_type = problem_type

        # update config.config with runner and pipeline config. 
        # Needs to be done in this order to keep config precedence
        omega_conf = OmegaConf.create(config)
        OmegaConf.update(omega_conf, "config", 
                         utils.copy_config_into(self.config, 
                                                utils.copy_config_into(pipeline_conf, runner_conf)
                                                )
                        )
           # copy config into the default config
        config = utils.copy_config_into(omega_conf, self.__DEFAULT_CONF__)
        
        #Now we validate config to make sure the component has everything it needs
        self._validate_conf(omega_conf, components)

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

    def log(self, msg, level="INFO"): 
        utils.log(self, msg, level)

    def notify(self, msg, level="ERROR"): 
        self.notifier.notify(msg, level)
        self.log("Notification Sent: %s" %msg, level)

    #helper function to lookup config key in component, pipeline or runner conf
    def _get_config(self, key, default_value=None):
        key = key.lower()
        value = utils.lower_conf(self.config).get(key, None)
        if not value: 
            value = utils.lower_conf(self.pipeline_conf).get(key, None)
            if not value: 
                value = utils.lower_conf(self.runner_conf).get(key, default_value)
        return value
