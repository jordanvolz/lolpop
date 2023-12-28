
If you've made it this far, you're likely considering writing a custom decorator to apply to a workflow. This may be an custom [cache_manager](base_cache_manager.md) or maybe an entirely new integration all together. Congratulations and we hope you'll enjoy the experience. Let's dig in. 


## Why Use Decorators? 

Python decorators wrap normal python functions or methods and modify their behavior. For example, almost all built-in components in lolpop are wrapped in `lolpop.utils.common_utils.log_execution`. This is a wrapper function that logs the start and end of a method to a `lolpop` `Logger` class, as well as the runtime. 

Decorators are powerful, as they can modify the existing functions behavior. For example, we leverage [cache_managers](base_cache_manager.md) to skip running methods all together if the method input hasn't changed as its output has already been saved to the cache. You might also opt to integrate with an external orchestration tool via decorators in lolpop.

Be careful when using decorators, they can have unintended consequences and you should only travel down this path if you're sure of what you are doing. 

## How to Write a Custom Decorator

Writing custom decorators in lolpop is relatively easy and straightforward. We'll assume you already know how to write a normal python decorator. What you'll then need to do is simply write a custom lolpop [component](building_extensions.md)where one of your class methods should be a decorator. 

In your custom component, you'll also want to include the default configuration `decorator_method` and the value should be the name of the class method that is the decorator you wish to use. 

## How to Use a Custom Decorator

To use a custom decorator, you'll add a new section to your workflow yaml: `decorators`. This section you'll then fill out as usual, with the abstract integration name and the class you wish to implement, as shown below: 

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

Note, you can include configuration for your decorator/component as normal via `<integration_name>.config` in the yaml file. This will be loaded into the decorator and will be available during the runtime of the `decorator_method`. 

And that's it! lolpop internally will process all decorators and will apply them to all relevant methods. By default, lolpop applies your decorator to all component methods. You can modify this default behavior via the `integration_types` and `integration_classes` configuration in your decorator config. `integration_types` takes a list of integration types to apply to: "component" and "pipeline". If you wish to apply a decorator to a runner class, you should do that manually in your own runner class. `integration_classes` is an explicit list of class names to apply the decorator to. You can otherwise control how the decorator is applied via including that logic in the decorator itself. 
