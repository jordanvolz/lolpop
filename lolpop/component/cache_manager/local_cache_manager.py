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
                   "cache_integration_types": ["component"]}
    }

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        self.cache_dir = Path(self._get_config("cache_dir"))
        os.makedirs(self.cache_dir, exist_ok=True)

    def cache(self, key, value, *args, **kwargs):
        file = self.cache_dir / key
        if callable(value): 
            value = getsource(value)
        joblib.dump(value,file)
        self.log("Wrote file %s to cache." %file, level="DEBUG")
        return file 

    def retrieve(self, key, *args, **kwargs): 
        out = None
        file = self.cache_dir / key
        try: 
            out = joblib.load(file)
            self.log("Cache hit for file %s" % file, level="DEBUG")
        except: #if file doesn't exist, it's the first time, so just pass 
            pass 

        return out 
         
