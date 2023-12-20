from lolpop.component.cache_manager.base_cache_manager import BaseCacheManager
from lolpop.utils import common_utils as utils
from pathlib import Path
from inspect import getsource 
import os 
import joblib


@utils.decorate_all_methods([utils.error_handler])
class LocalCacheManager(BaseCacheManager):

    __DEFAULT_CONF__ = {
        "config": {"cache_dir" : "/tmp/cache", 
                   "decorator_method": "cache_decorator",
                   "integration_types": ["component"]}
    }

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        self.cache_dir = Path(self._get_config("cache_dir"))
        os.makedirs(self.cache_dir, exist_ok=True)

    def cache(self, key, value, *args, **kwargs):
        """Caches the value for the given key.

        The value can be any object. If the value is a callable, its source code will be stored instead.
        The key determines the filename under which the value will be stored.

        Args:
            key (str): The key to associate with the value.
            value (object): The value to be cached.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            str: The path to the cached file.

        Raises:
            None.
        """
        file = self.cache_dir / key
        if callable(value): 
            value = getsource(value)
        try: 
            joblib.dump(value,file)
            self.log("Wrote file %s to cache." %file, level="DEBUG")
        except Exception as e: 
            self.log("Unable to cache %s to %s: %s. Subsequent workflow runs will have to recompute this value" %(value, file, str(e)), level="WARN")
        return file 

    def retrieve(self, key, *args, **kwargs): 
        """Retrieves the cached object for the given key.

        If the cached file exists, it will be loaded and returned as an object.
        If the cached file doesn't exist, None will be returned.

        Args:
            key (str): The key associated with the cached object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            object: The cached object for the given key, or None if it doesn't exist.

        Raises:
            None.
        """
        out = None
        file = self.cache_dir / key
        try: 
            out = joblib.load(file)
            self.log("Cache hit for file %s" % file, level="DEBUG")
        except: #if file doesn't exist, it's the first time, so just pass   # noqa: E722
            pass 

        return out 
         
