from lolpop.component.base_component import BaseComponent
from lolpop.utils import common_utils as utils
from typing import Any
from functools import wraps
from hashlib import md5

class BaseCacheManager(BaseComponent):

    __DEFAULT_CONF__ = {
        "config": {
            "decorator_method": "cache_decorator", 
            "integration_types" : ["component"]
        }
    }

    def cache(self, key, value, *args, **kwargs) -> str:
        pass

    def retrieve(self, key, *args, **kwargs) -> Any: 
        pass 

    def equals(self, objA, objB, *args, **kwargs) -> bool: 
        return utils.compare_objects(objA, objB)

    def cache_decorator(self, func, cls): 
        @wraps(func)
        def wrapper(*args, **kwargs):
            obj = args[0] #object should always be first argument
            base_key = self._stringify_input(obj, func, args, kwargs)
            class_name=obj.name
            cache_integration_types = self._get_config("integration_types", ["component"])
            cache_integration_classes = self._get_config("integration_classes", [])
            if cache_integration_classes is not None and len(cache_integration_classes) > 0: 
                apply_cache = class_name in cache_integration_classes
            else: 
                apply_cache = obj.integration_type in cache_integration_types
            obj.log("Checking cache for %s" %base_key, level="DEBUG")
            if (not obj._get_config("skip_cache", False)) and (apply_cache):
                try:
                    skip_func = True
                    # first check args and kwargs to see if there is any difference
                    # between what is provided and what is in the cache
                    i = 1  
                    for arg in args[1:]:  # start at 1 to skip self
                        cache_obj = self.retrieve(f"{base_key}__arg_{str(i)}")
        
                        if not self.equals(cache_obj, arg): 
                            skip_func=False
                            obj.log("Cached object not equivalent for argument %s" %i, level="DEBUG")
                            break 
                        i+=1

                    if skip_func: 
                        for key,val in kwargs.items():
                            cache_obj = self.retrieve(key=f"{base_key}__{key}")
                            if not self.equals(cache_obj,val): 
                                skip_func = False 
                                obj.log("Cached object not equivalent for keyword argument %s" %key, level="DEBUG")
                                break 

                    #also check if the function has changed
                    if skip_func: 
                        cache_obj = self.retrieve(f"{base_key}__{func.__name__}")
                        if not self.equals(cache_obj, func): 
                            skip_func = False 
                            obj.log("Cached function not eqivalent for %s" %func.__name__, level="DEBUG")

                    #and check the component config 
                    if skip_func: 
                        cache_obj = self.retrieve(f"{base_key}__config")
                        if not self.equals(cache_obj, obj.config):
                            skip_func = False
                            obj.log("Cached config not equivalent for %s" %class_name, level="DEBUG")

                    #and finally, check that the output exists
                    if skip_func: 
                        output = self.retrieve(f"{base_key}__output")
                        if output is None: 
                            skip_func = False
                            obj.log("Cached output doesn't exist for %s" %base_key, level="DEBUG")

                    if not skip_func:  
                        obj.log("Insufficient cache hits to skip function %s. Executing %s.%s as normal." %(base_key, class_name, func.__name__), level="DEBUG")

                        #we detected something was different, so run the function and then cache all objects 
                        output = func(*args, **kwargs)
                        #Note: we should only cache new input values after the function successfully runs,
                        # otherwise you will skip it on the next iteration. 

                        i = 1
                        for arg in args[1:]: 
                            self.cache(f"{base_key}__arg_{str(i)}", arg)
                            i+=1

                        for key, value in kwargs.items(): 
                            self.cache(f"{base_key}__{key}", value)

                        self.cache(f"{base_key}__{func.__name__}", func)
                        self.cache(f"{base_key}__config", obj.config)
                        self.cache(f"{base_key}__output", output)

                        obj.log("Successfully cached all inputs and outputs to %s" %base_key, level="DEBUG")

                        return output 
                    else: 
                        obj.log("Detected no changes to input or function for %s Retrieving output from cache." %base_key, level="INFO")
                        return output 
 
                except Exception as e:
                    #prevent unnecessary nesting
                    if str(e).startswith("An error occurred:"):
                        raise e
                    else:
                        raise Exception(f"An error occurred: {e}")
            else: #component has a skip_cache flag, so we'll just short circuit
                obj.log("Cache criteria not met for %s. Running method as normal" % base_key, level="DEBUG")
                return func(*args, **kwargs)
        return wrapper

    #hacky attempt to make inputs map to a unique value
    def _stringify_input(self, obj, func, args, kwargs) -> str: 
        base = f"{obj.name}_{func.__name__}"
        output = base 
        for arg in args: 
            output = f"{output}_a-{utils.convert_arg_to_string(arg)}"
        for k,v in kwargs.items(): 
            output = f"{output}_k-{k}-{utils.convert_arg_to_string(v)}"
        for k,v in obj.config.items(): 
            output = f"{output}_c-{k}-{utils.convert_arg_to_string(v)}"

        #escape slashes
        output = output.replace("/", ".")
        #mac os only allows 256 characters in file names by default
        #lower to 200 to give room for kwarg names
        if len(output)>200:
            output = f"{base}_{md5(output.encode('UTF-8')).hexdigest()}"
        return output 

