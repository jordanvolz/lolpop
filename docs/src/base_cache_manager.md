## Overview

A `cache_manger` is a component that is able to cache inputs and outputs to class methods. This functionality is intended for use in development workflows to iterate quickly on troublesome areas of the workflow so that parts of the pipeline can be skipped if the inputs have not changed. In these cases, a cache manager will be able to retrieve results from the cache instead of executing the method again. 

The `BaseCacheManager` class provides an interface and some default methods that child classes can utilize to implement method caching. In particular, child classes should mainly be looking to implement `cache` and `retrieve` methods in order ot determine how to save and load data, and possibly also implement a more robust `equals`, depending on their use case. 

Also be sure to check out [Using Decorators](using_custom_decorators.md) to learn more about using decorators in your own workflows. 

!!! Note 
    The `cache_manager` is considered experimental and is not recommended for production use. It is only recommended to use to help accelerate debugging development workflows. 

## Attributes

`BaseCacheManager` contains no default attributes. 

## Configuration

### Required Configuration 

`BaseHyperparameterTuner` contains no required configuration or components.
 
### Optional Configuration

`BaseCacheManager` has the following optional configuration: 

- `integration_class`: A list of class names to decorate with the cache `decorator_method`. You can use this to explicitly cache certain classes in your workflow. Note that this overrides `integration_types`, but is also overridden by a class's own `no_cache` configuration. 

### Default Configuration

`BaseCacheManager` uses the following default configuration: 

- `decorator_method`: The method to use to decorate class methods so that they are cached after execution. Defaults to `cache_decorator`. This should not be changed unless you really know what you are doing 

- `integration_types`: The integration type(s) to decorate with the cache `decorator_method`. This defaults to `["component"]` and it is only recommended to cache at the component level. 


## Interface

The following methods are part of `BaseCacheManager` and should be implemented in any class that inherits from this base class: 

### cache

This method takes a key value pair and caches the value using the specified key. You can then retrieve the value from the cache given the key by using `retrieve` 

```python
def cache(self, key, value, *args, **kwargs) -> str
```

**Arguments**: 

- `key` (str): The key to use to cache the data 
- `value` (object): The object to cache.  

**Returns**:

- `str`: This is intended to be the location of the object in the cache itself. I.E. a folder location or bucket location, etc. 

### retrieve

This method retrieves a cached object from the cache given the provied key.

```python
def retrieve(self, key, *args, **kwargs) -> Any
```

**Arguments**: 

- `key` (str): The key of the cached object. 

**Returns**:

- `object`: This is an object that was stored in the cache via `cache`

## Default Methods

The following are default methods that are implemented in the base class. They can be overridden by inheriting classes as needed. 

### equals

This method compares two objects to determine if they are equal. This utilizes `lolpop.utils.common_utils.compare_objects` which is a "quick and dirty" method to compare objects. If you desire a more robust method you may wish to override this method. 

```python
def equals(self, objA, objB, *args, **kwargs) -> bool
```

**Arguments**: 

- `objA` (object): The first object.
- `objB` (object): The second object.

**Returns**:

- `bool`: whether the two objects are equal. 


### cache_decorator

This is a default decorator which can be used to cache objects. This should be sufficient for any class inheriting from `BaseCacheManager`, given that they implement non-trivial `cache` and `retrieve`.

lolpop will decorate any classes in this decorate as specified in `integration_types` or `integration_classes`. Methods in wrapped classes will then operate as follows: 

- When the method is executed, the cache will be checked for all of the following: 

    1. Input arguments 
    2. Input keyword arguments 
    3. The configuration of the integration
    4. The actual method code

- Each of the above is compared to the currently executing method. If no differences are found then the output of the method is retrieved from the cache and returned. 

- If no previous output is found or if differences are found in the method inputs, configuration, or code itself, then lolpop will execute the method as normal and return the output. 

- If the method is executed then the method inputs, configuration, code, and output are all cached. 

!!! Note 
    `cache_decorator` should be applied either via `decorators` when defining your workflow [decorators][using_custom_dectorators.md] in your workflow `yaml` file, or directly to integrations via the `lolpop.utils.common_utils.decorate_all_methods` class decorator. 

```python
def cache_decorator(self, func, cls): 
```

## _stringify_input

Helper function that converts method inputs to strings. This is used to properly map all inputs of a method call into a string and to try to ensure that unique calls of the method also are mapped to unique values (in the case that a method might be called multiple times during a workflow).

This attempts to form a string by calling `lolpop.utils.common_utils.convert_arg_to_string` on every argument, keyword argument, and configuration items of the calling method. The resulting string will also be hashed if it is longer than 200 characters. 

```python
def _stringify_input(self, obj, func, args, kwargs) -> str:
```

**Arguments**: 

- `obj` (object): The integration object that is being used. 
- `func` (function): The method of the integration object that is being executed
- `args` (list): A list of arguments passed into `func`
- `kwargs` (dict): A dictionary of keyword arguments passed into `func`

**Returns**:

- `str`: A string representing this particular execution of `func`



## Usage 

```yaml hl_lines="10 11"
pipeline: 
  process: OfflineProcess 
  train: OfflineTrain
  predict: OfflinePredict
component: 
  metadata_tracker: MLFlowMetadataTracker
  notifier: StdOutNotifier
  resource_version_control: dvcVersionControl
  metrics_tracker: MLFlowMetricsTracker
decorator: 
  cache_manager: LocalCacheManager
... 

cache_manager: 
    config: 
        decorator_method: cache_decorator
        integration_types: ["component"]
...


```