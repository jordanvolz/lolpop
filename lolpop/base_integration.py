from lolpop.utils import common_utils as utils
from anytree import AnyNode, RenderTree
from omegaconf import dictconfig, OmegaConf
import os  
from inspect import currentframe

class BaseIntegration: 

    __REQUIRED_CONF__ = {
        "config": []
    }
    __DEFAULT_CONF__ = {
        "config": {}
    }

    __DEFAULT_INT__ = {
        "component": {
            "logger": "StdOutLogger",
            "notifier": "StdOutNotifier",
            "metadata_tracker": "MLFlowMetadataTracker",
        }
    }
    
    suppress_logger = False
    suppress_notifier = False

    def __init__(self, 
                 conf=None, 
                 parent=None, 
                 integration_type=None, 
                 integration_framework=None, 
                 problem_type="Unknown", 
                 skip_config_validation=False, 
                 dependent_integrations=None, 
                 decorators=None,
                 plugin_mods=None, 
                 plugin_paths=None,
                 is_standalone=False,
                 *args, **kwargs):     
        
        if dependent_integrations is None: 
            dependent_integrations = {}
        if decorators is None: 
            decorators = []
        if plugin_mods is None: 
            plugin_mods = []
        if plugin_paths is None: 
            plugin_paths = []

        # Integration name. Mainly going to be used for referring to this during logging, etc. 
        # self.name = class name
        self.name = type(self).__name__

        # self.module = module. 
        # Built in modules should have the structure: 
        # lolpop.<integration_type>.<type>.<module>, such as: 
        # lolpop.component.metadata_tracker.mlflow_metadata_tracker
        self.module = self.__module__
        
        #figure out what type of integration we are? I.E. runner, pipeline, component, etc. 
        self.integration_type = integration_type
        if self.integration_type is None:
            try:
                self.integration_type = self.module.split(".")[-3]
            except:  # noqa: E722
                self.integration_type = "extension"

        #figure out what type of integration type we are. 
        # i.e. if you are a "runner" then we want to know what "runner_type" you are
        try:
            int_type = self.module.split(".")[-2]
        except:  # using some kind of custom class  # noqa: E722
            int_type = self.module
        self.type = int_type
        #setattr(self, "%s_type" %self.integration_type, int_type)

        #set parent object 
        self.parent = parent 
        self.parent_integration_type = None
        if self.parent is not None:
            self.parent_integration_type = parent.integration_type
        self.problem_type = problem_type
        if (self.problem_type == "Unknown" or self.problem_type is None) and self.parent is not None: 
            self.problem_type = self.parent.problem_type

        #get configuration 
        config = utils.get_conf(conf)
        
        #set up integration framework
        self.integration_framework = integration_framework
        if self.integration_framework is None:
            integration_framework = config.get("integration_framework", {})
            if len(integration_framework) > 0: #framework provided via conf
                self.integration_framework = _get_integration_framework_tree(integration_framework)
            elif self.parent is None and not is_standalone: # no parent, so assume we are at the root and get the default
                self.integration_framework = _get_default_integration_framework()
            else: #no framework provided and we have a parent, so not root, assume we are being dynamically created somewhere, so don't try to traverse the framework
                pass 

        #handle config    
        config = utils.resolve_conf_variables(config)
        valid_conf = OmegaConf.create(config).copy() 
        #set the integration config before we start copying parent config in. 
        #This saves the integration config as whatever is passed in + the default config
        self.config = utils.copy_config_into(valid_conf.get("config", {}), self.__DEFAULT_CONF__.get("config", {}))
        #handle all the configuration inheritance
        OmegaConf.update(
            valid_conf, 
            "config", 
            _inherit_config(
                valid_conf.get("config",{}),
                self.__DEFAULT_CONF__.get("config",{}),
                self
            )
        )

        #validate configuration to ensure we have all requirements
        if not skip_config_validation:
            self._validate_conf(valid_conf, dependent_integrations)

        #handle plugins
        if len(plugin_mods) == 0:
            if len(plugin_paths) == 0:
                plugin_paths = self._get_config("plugin_paths", [])
            file_path = None
            if hasattr(self, "__file_path__"):
                file_path = self.__file_path__
            plugin_mods = utils.get_plugin_mods(self, plugin_paths, file_path)
        self.plugin_mods = plugin_mods

        #set up default integrations
        dependent_integrations = utils.set_up_default_integrations(
                                    self, 
                                    valid_conf, 
                                    self.__DEFAULT_INT__,
                                    plugin_mods=plugin_mods,
                                    skip_config_validation=skip_config_validation,
                                    dependent_integrations=dependent_integrations
                                    )


        #set up decorators
        decorators = decorators + utils.set_up_decorators(
            self, valid_conf, plugin_mods=plugin_mods, dependent_integrations=dependent_integrations
            )
        
        #if we're at the root of our framework, we have to apply decorators here,
        # otherwise, things will be applied when they registered below
        if  (self.integration_framework is not None) and (self.integration_framework.is_root): 
            self = utils.apply_decorators(self, decorators, integration_type=self.integration_type)
    
        #set all passed in integrations 
        for integration_type in dependent_integrations.keys():
            for integration in dependent_integrations.get(integration_type).keys(): 
                setattr(self, integration, dependent_integrations.get(integration_type).get(integration))

        #process children
        if self.integration_framework is not None: 
            for child in self.integration_framework.children:
                self.log("Processing node %s in %s integration framework..." %(child.id, self.integration_type))
                processed_integrations = {}

                #id of the node in the intergration framework should be the integration type
                child_integration_type = child.id
                #pop off config so it's not processed as an integration
                integration_config = config.get(child_integration_type, {}).pop("config",{})

                for integration in config.get(child_integration_type, {}).keys():
                    #skip registration if the integration already exists in the default_integrations
                    if integration not in self.__DEFAULT_INT__.get(child_integration_type, {}).keys():
                        self.log("Declared %s integration: %s. Processing..." % (child_integration_type, integration))

                        obj = utils.register_integration_class(self, 
                                                                config, 
                                                                integration,
                                                                integration_type=child_integration_type,
                                                                integration_framework=child,
                                                                problem_type=self.problem_type, 
                                                                dependent_integrations=dependent_integrations,
                                                                plugin_mods=plugin_mods,
                                                                decorators=decorators,
                                                                skip_config_validation=skip_config_validation)
                        if obj is not None: 
                            self.log("Loaded class %s into %s %s" %(type(getattr(self,integration)).__name__, child_integration_type, integration))
                            processed_integrations[integration] = obj
                        else: 
                            self.log("Unable to load class for %s: %s" %(child_integration_type, integration))
                    else: 
                        self.log("Integration %s already in default integrations. Skipping..." %integration)

                ##if integration is a leaf then we need to update other integrations with the full set
                #if child.is_leaf: 
                #    for obj in processed_integrations.values(): 
                #        obj._update_integrations(integrations=processed_integrations)

                #check to see if we want to pass integrations to siblings
                if integration_config.get("pass_integration_to_siblings", True):
                    #add processed integrations to the dependent list so they get passed down.
                    self.log("Updating dependent integrations with all processed child integrations in integration %s. All sibling integrations will have access to processed integrations: %s" %(child.id, str(list(processed_integrations.keys()))), level="DEBUG")
                    if child.id not in dependent_integrations.keys(): 
                        dependent_integrations[child.id] = processed_integrations
                    else: #update existing integration type 
                        dependent_integrations[child.id].update(processed_integrations)
                else: 
                    self.log("Detected that sibling integration pass down is disabled for integration %s. Siblings will not be updated with processed integrations: %s." %(child.id, str(list(processed_integrations.keys()))), level="DEBUG")

                #check to sese if we need to update other integrations with the full set
                # defaults to true if the child is a leaf
                if integration_config.get("update_peer_integrations", child.is_leaf):
                    self.log("Updating all peer integrations for integration %s." % child.id, level="DEBUG")
                    for obj in (list(processed_integrations.values()) + 
                                [v for k,v in dependent_integrations[child.id].items() if k in self.__DEFAULT_INT__.get(child.id,{}).keys()]):
                        obj._update_integrations(integrations=processed_integrations)
                else: 
                    self.log("Detected that peer integration updating is disabled for integration %s. Peer integrations will not be updated." %child.id,level="DEBUG")

    def _update_integrations(self, integrations=None, *args, **kwargs):
        if integrations is None: 
            integrations = {} 
        for integration in integrations.keys():
            setattr(self, integration, integrations.get(integration))

    def _validate_conf(self, conf, dependent_integrations):
        integrations=dependent_integrations.copy()   
        missing, total_missing = utils.validate_conf(conf, self.__REQUIRED_CONF__)
        if total_missing > 0:
            #check to see if missing integrations are passed in
            for integration_type in missing.keys(): 
                missing_found = []
                for integration in missing.get(integration_type): 
                    #make sure to check for class-specific requirements
                    integration_key=integration
                    if "|" in integration_key:
                        integration_key = integration_key.split("|")[0]
                    if integrations.get(integration_type, {}).get(integration_key) is not None:
                        #if missing int is part of passed in dependent ints, then decrement count and remove from missing
                        total_missing = total_missing - 1
                        missing_found.append(integration)
                #need to remove after the above loop so you don't mess up the indices in the middle of a traversal
                for key in missing_found: 
                    missing[integration_type].remove(key)
            if total_missing > 0:
                raise Exception("Missing the following from %s configuration: %s" % (
                    type(self).__name__, missing))

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

        #if value wasn't found, check in parent
        if value is None and self.parent is not None: 
            value = self.parent._get_config(key)
        
        #if no value found in parent, check environment
        if value is None: 
            value = os.getenv(key,default=default_value)
        
        return value
        
    def _set_config(self, key, value): 
        key = key.lower()
        self.config[key]=value

    def _print_integration_framework(self): 
        if hasattr(self, "integration_framework"):
            print(RenderTree(self.integration_framework))
        else: 
            print("Object has no integration framework defined.")

    def _print_integrations(self): 
        if hasattr(self, "integration_framework"):
            print("Integrations attached to %s %s:" %(self.integration_type, self.name))
            for child in self.integration_framework.children: 
                integration_type = child.id 
                print("\n %s" %integration_type)
                for integration in [x for x in dir(self) if (not x.startswith("_") and hasattr(getattr(self,x),"integration_type"))]:
                    int_obj = getattr(self, integration)
                    if getattr(int_obj,"integration_type") == integration_type: 
                        print(" -- %s (%s)" %(integration, int_obj.name))
        else:
            print("Object has no integration framework defined.")




def _get_default_integration_framework():
    runner = AnyNode(id="runner")
    global_component = AnyNode(id="component", parent=runner)
    pipeline = AnyNode(id="pipeline", parent=runner)
    component = AnyNode(id="component", parent=pipeline)
    return runner


def _get_integration_framework_tree(framework_conf, parent=None):
    if len(framework_conf) > 1 and parent is None: 
        raise Exception("ERROR: Detected more than one root node in integration framework. You may only have one one root node in your integration framework tree. Found root nodes: %s" %str(framework_conf.keys()))
    node = AnyNode()
    for k, v in framework_conf.items():
        node = AnyNode(id=k)
        if parent is not None:
            node.parent = parent
        if isinstance(v, dictconfig.DictConfig):
            _ = _get_integration_framework_tree(v, parent=node)
    return node


def _inherit_config(conf, default_conf, integration, conf_array=None):

    if conf_array is None: 
        conf_array = []

    parent = integration.parent 

    #parent exists, so we need to iterate
    if parent is not None: 
        conf_array.append(parent.config)
        return _inherit_config(conf, default_conf, parent, conf_array=conf_array)
    else: #no parent, so we can stop
        conf_array.append(conf)
        final_conf = default_conf

        for c in conf_array: 
            final_conf = utils.copy_config_into(c, final_conf)

        return final_conf 