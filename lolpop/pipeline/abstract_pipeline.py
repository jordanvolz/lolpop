from lolpop.utils import common_utils as utils
from omegaconf import OmegaConf
class AbstractPipeline: 

    __REQUIRED_CONF__ = {
        "components": [], 
        "config": []
    }
    __DEFAULT_CONF__ = {
        "config" : {}
    }

    suppress_logger = False
    suppress_notifier = False

    def __init__(self, conf, runner_conf, parent_process="runner", problem_type=None, pipeline_type="abstract_pipeline", components={}, plugin_mods=[], **kwargs):
        #set basic properties like configs
        self.name = type(self).__name__
        self.config = conf.get("config", {})
        self.parent_process = parent_process
        self.pipeline_type = pipeline_type
        self.runner_conf = runner_conf
        self.problem_type = problem_type

        #merge pipeline conf into runner conf
        omega_conf = OmegaConf.create(conf)
        OmegaConf.update(omega_conf, "config",
                         utils.copy_config_into(self.config, runner_conf)
                         )

        #merge into default conf & validate the result
        conf = utils.copy_config_into(omega_conf, self.__DEFAULT_CONF__)
        self._validate_conf(omega_conf, components)

        #set up reference to each component that is passed in from runner. 
        for component in components.keys(): 
            setattr(self, component, components.get(component))

        pipeline_conf = self.config
        pipeline_conf["pipeline_type"]=self.pipeline_type

        #now handle all components explicitly set for pipeline
        #note: this will override any component name inherited from the runner, which is what we want
        pipeline_components = {}
        if "components" in conf.keys(): 
            for component in conf.components.keys(): 
                obj = utils.register_component_class(self, conf, component, pipeline_conf = pipeline_conf, runner_conf = runner_conf, parent_process=self.name, problem_type = self.problem_type, dependent_components=components, plugin_mods=plugin_mods)
                if obj is not None: 
                    self.log("Loaded class %s into component %s" %(type(getattr(self, component)).__name__, component))
                    pipeline_components[component] = obj
                else: 
                    self.log("Unable to load class for component %s" %
                             component)

        #now update all pipeline scope components to know about the other pipeline components
        for obj in pipeline_components.values(): 
            obj._update_components(components = pipeline_components)

    def _validate_conf(self, conf, components):
        missing, total_missing = utils.validate_conf(conf, self.__REQUIRED_CONF__, components)
        if total_missing > 0: 
            #check to see if missing components are provided by runner via kwargs
            if len(missing.get("components")) > 0: 
                for component in missing.get("components"): 
                    if components.get(component, None) is not None: 
                        total_missing = total_missing - 1
            if total_missing > 0:   
                raise Exception ("Missing the following from pipeline configuration: %s" %missing)

    def log(self, msg, level="INFO"): 
        if not self.suppress_logger: 
            utils.log(self, msg, level)

    def notify(self, msg, level="ERROR"): 
        if not self.suppress_notifier: 
            self.notifier.notify(msg, level)
            self.log("Notification Sent: %s" %msg, level)

    #helper function for lookup up config key in pipeline or runner conf
    def _get_config(self, key, default_value=None): 
        key = key.lower()
        value = utils.lower_conf(self.config).get(key, None)
        if not value: 
            value = utils.lower_conf(self.runner_conf).get(key, default_value)
        return value 