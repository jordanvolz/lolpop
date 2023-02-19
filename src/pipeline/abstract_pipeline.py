from utils import common_utils as utils

class AbstractPipeline: 

    __REQUIRED_CONF__ = {
        "components": [], 
        "config": []
    }
    __DEFAULT_CONF__ = {
        "config" : {}
    }

    def __init__(self, conf, runner_conf, parent_process="runner", problem_type=None, pipeline_type="abstract_pipeline", **kwargs):
        #config defines all components in `components`
        #format is 
        ## <pipeline>: 
        ##   components: 
        ##     <component>: <class>
        # then you need to also have a directory <component> with has your class loaded top-level
        self.name = type(self).__name__
        conf = utils.copy_config_into(conf, self.__DEFAULT_CONF__)
        self._validate_conf(conf, kwargs.get("components"))
        self.config = conf.get("config", {}) 
        self.parent_process = parent_process
        self.pipeline_type = pipeline_type
        self.runner_conf = runner_conf
        self.problem_type = problem_type

        #set up reference to each component that is passed in from runner. 
        for component in kwargs.get("components",{}).keys(): 
            setattr(self, component, kwargs.get("components").get(component))

        pipeline_conf = self.config
        pipeline_conf["pipeline_type"]=self.pipeline_type

        #now handle all components explicitly set for pipeline
        #note: this will override any component name inherited from the runner, which is what we want
        pipeline_components = {}
        if "components" in conf.keys(): 
            for component in conf.components.keys(): 
                obj = utils.register_component_class(self, conf, component, pipeline_conf = pipeline_conf, runner_conf = runner_conf, parent_process=self.name, problem_type = self.problem_type, dependent_components=kwargs.get("components"))
                self.log("Loaded class %s into component %s" %(type(getattr(self, component)).__name__, component))
                pipeline_components[component] = obj

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
        utils.log(self, msg, level)

    def notify(self, msg, level="ERROR"): 
        self.notifier.notify(msg, level)
        self.log("Notification Sent: %s" %msg, level)

    #helper function for lookup up config key in pipeline or runner conf
    def _get_config(self, key, default_value=None): 
        key = key.lower()
        value = utils.lower_conf(self.config).get(key, None)
        if not value: 
            value = utils.lower_conf(self.runner_conf).get(key, default_value)
        return value 