# LocalCacheManager

The `LocalCacheManager` class is a subclass of `BaseCacheManager` and provides methods for caching and retrieving objects locally.

## Attributes

`LocalCacheManager` contains the following attributes: 

- `cache_dir`: The location of the cache directory, as specified in the component configuration. 

## Configuration

### Required Configuration

`LocalCacheManager` has no required configuration.

### Optional Configuration 

`LocalCacheManager` has the following optional configuration: 

- `integration_class`: A list of class names to decorate with the cache `decorator_method`. You can use this to explicitly cache certain classes in your workflow. Note that this overrides `integration_types`, but is also overridden by a classes' own `no_cache` configuration. 

### Default Configuration 

`LocalCacheManager` uses the following default configuration: 

- `cache_dir` : The directory to use for the cache. This is the top most directory into which `LocalCacheManager` will create other sub-directories. Defaults to `/tmp/cache` 

- `decorator_method`: The method to use in `LocalCacheManager` to decorate class methods so that they are cached after execution. Defaults to `cache_decorator`. This should not be changed unless you really know what you are doing 

- `integration_types`: The integration type(s) to decorate with the cache `decorator_method`. This defaults to `["component"]` and it is only recommended to cache at the component level. 


### cache 
This method caches the provided value with the given key.

The value can be any object. If the value is a callable, its source code will be stored instead. The key determines the filename under which the value will be stored.

```python
def cache(self, key, value, *args, **kwargs): 
```

#### Arguments

- `key` (str): The key to associate with the value.
- `value` (object): The value to be cached.

#### Returns

- `str`: The path to the cached file.


### retrieve 
This method retrieves the cached object for the given key.

If the cached file exists, it will be loaded and returned as an object. If the cached file doesn't exist, None will be returned.

```python 
def retrieve(self, key, *args, **kwargs)
```

#### Arguments

- `key` (str): The key associated with the cached object.

#### Returns

- `object`: The cached object for the given key, or None if it doesn't exist.



## Usage

```python
from lolpop.component import LocalCacheManager

config = {
    # insert component configuration 
}
cache_manager = LocalCacheManager(conf=config)

_ = cache_manager.cache("my_key", myObj)

cached_obj = cache_manager.retrieve("my_key")

assert cache_manager.equals(myObj,cached_obj)
```