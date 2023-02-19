from utils import common_utils as utils

class AbstractComponent: 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    __DEFAULT_CONF__ = {
        "config" : {}
    }

    def __init__(self, config={}, pipeline_conf={}, runner_conf={}, parent_process=None, problem_type = None, **kwargs):
        self.name = type(self).__name__
        config = utils.copy_config_into(config, self.__DEFAULT_CONF__)
        self._validate_conf(config,kwargs.get("components",{}))
        self.config = config.get("config",{})
        self.pipeline_conf = pipeline_conf
        self.runner_conf = runner_conf
        self.parent_process = parent_process
        self.problem_type = problem_type
        for component in kwargs.get("components",{}).keys(): 
            setattr(self, component, kwargs.get("components").get(component))
        
    def _update_components(self, **kwargs): 
        for component in kwargs.get("components",{}).keys(): 
            setattr(self, component, kwargs.get("components").get(component))

    def _validate_conf(self, conf, components):
        missing, total_missing = utils.validate_conf(conf, self.__REQUIRED_CONF__, components)
        if total_missing>0: 
            #check to see if missing components are provided by runner via kwargs
            if len(missing.get("components",{})) > 0: 
                for component in missing.get("components"): 
                    if components.get(component, None) is not None: 
                        total_missing = total_missing - 1
                if total_missing > 0:   
                    raise Exception ("Missing the following from pipeline configuration: %s" %missing)

    def log(self, msg, level="INFO"): 
        utils.log(self, msg, level)

    def notify(self, msg, level="ERROR"): 
        self.notifier.notify(msg, level)
        self.log("Notification Sent: %s" %msg, level)

    #hdlper function to lookup config key in component, pipeline or runner conf
    def _get_config(self, key, default_value=None):
        key = key.lower()
        value = utils.lower_conf(self.config).get(key, None)
        if not value: 
            value = utils.lower_conf(self.pipeline_conf).get(key, None)
            if not value: 
                value = utils.lower_conf(self.runner_conf).get(key, default_value)
        return value
