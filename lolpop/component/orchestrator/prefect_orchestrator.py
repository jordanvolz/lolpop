from lolpop.component.orchestrator.base_orchestrator import BaseOrchestrator
from lolpop.utils import common_utils as utils
from functools import wraps
import os 

from importlib import reload 

@utils.decorate_all_methods([utils.error_handler])
class PrefectOrchestrator(BaseOrchestrator): 

    __DEFAULT_CONF__ = {
        "config": {
            "decorator_method": "prefect_decorator",
            "integration_types": ["runner", "pipeline", "component"], 
            "prefect_profile": "default",
            "prefect_flow_integration": ["runner", "pipeline"], 
            "prefect_task_integration": ["component"],
        }
    }

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        # check to see if env variables are set. 
        # in prefect env variables override profiles and are set in the root context so
        # there is no (non-super hacky) currently way to override them programatically
        # but we can at least provide a warning
        prefect_env_variables = [x for x in os.environ.keys() if x.startswith("PREFECT")]
        if len(prefect_env_variables)>0: 
            self.log("Found PREFECT_ configuration in the environment variables: %s. Environment variables override \
                     profile settings in Prefect. Consider unsetting these variables if their use is not intended." 
                     %str(prefect_env_variables), level="WARN")

        # we need to switch profiles before importing prefect. The reason being that prefect
        # sets the root context when imported to the active profile. The only way to change this
        # programatically is via prefect.context.use_profile and some context manager acrobatics, 
        # which is going to be complicated for lolpop. It's easier to just execute a profile switch
        profile = self._get_config("PREFECT_PROFILE")
        out, _ = utils.execute_cmd(["prefect", "profile", "use", profile])

        #if profile is new, then try to create it and apply settings
        if "not found" in out: 
            utils.execute_cmd(
                ["prefect", "profile", "create", profile])

            profile_settings = self._get_config("prefect_settings", {})
            for k, v in profile_settings.items():
                utils.execute_cmd(
                    ["prefect", "config", "set", f"{k}={v}"])

        self.log("Using prefect profile %s" %profile, level="INFO")

        #now we can import, and we'll also need to add them to globals
        from prefect import flow, task 
        globals()["flow"] = flow 
        globals()["task"] = task 

        #TODO: look into default flow/task params
        #TODO: set up deploymentments
        ##read into code a bit, maybe just another function from operator class to register?
        #TODO: other integraitons - prefect logger, results, artifacts, etc?


    def prefect_decorator(self, func, cls):
        @wraps(func)
        def prefect_wrapper(*args, **kwargs):
            obj = args[0]
            #wrap in flow
            if obj.integration_type in self._get_config("prefect_flow_integration"):
                flow_kwargs = self._get_config("flow_kwargs", {})
                deployment_kwargs = self._get_config("deployment_kwargs", {})
                return flow(func, **flow_kwargs)(*args, **kwargs)  # noqa: F821
            #wrap in task
            elif obj.integration_type in self._get_config("prefect_task_integration"):
                try: #skip wrapping things that are sub components. This will cause nested task error in prefect
                    if obj.parent_integration_type == "component": 
                        raise Exception("Detected task in a task. This is not allowed in prefect, so we'll attempt to run the function as normal.")
                    task_kwargs = self._get_config("task_kwargs",{})
                    return task(func, **task_kwargs)(*args,**kwargs)  # noqa: F821
                except Exception as e: 
                    return func(*args, **kwargs)
            else: #func gets decorated but it shouldn't be, do what's normal
                return func(*args, **kwargs)
        return prefect_wrapper
    
