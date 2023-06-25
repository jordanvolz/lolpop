
Building workflows in lolpop is quick, intuitive, and easy. Some might even say enjoyable! We'll assume you've already read through the [configuration](configuration.md) section and understand the basics of working with configuration and how to create them. 

Although it's possible to build entire workflows from [built-in](integrations.md) in lolpop, you might also find yourself wishing to build your own at some point in time. The [extensions](extensions.md) section covers everything you need to know in order to build your own components, pipelines, and runners. In this sections we'll focus more on how to glue everything together. This is a useful section to cover even if you don't plan to build your own components, as it will help you understand how lolpop operates in the off chance that you happen to need to read through the source code at some point and debug some strange error. 


## Working with Components

Components are built from a simple configuration: 

```yaml title="Reference component configuration"
config: 
    key: value
    ... 
```
 
Components can be built directly by instantiating their class with a proper configuration, although it's much more common to build them as part of a pipeline or runner.

```python
from lolpop.component import XGBoostModelTrainer

config_file = "/path/to/config_file.yaml" 
model_trainer = XGBoostModelTrainer(conf=config_file)
... 
```

When operating within a component class, you can retrieve any configuration that is passed in via: 

```python
config_value = self._get_config("config_key")
```

Furthermore, components can access any other global component, or local pipeline component via: 

```python
self.component_type
```

When constructing objects, lolpop will make all other global and pipeline-local components available to each pipeline and component. So, for example, let's say that a runner has the following configuration: 

```yaml
pipelines: 
    ...
components: 
    metadata_tracker: MyMetadataTracker
    metrics_tracker: MyMetricsTracker
...
```

Then, any other component in this runner can access `MyMetadataTracker` and `MyMetricsTracker` via: 

```python
my_metadata_tracker = self.metadata_tracker
my_metrics_tracker = self.metrics_tracker
```
!!! Note 
    There's no white list for component type names. You can name them whatever you want. 

This allows you to easily access other components without knowing how to instantiate them, and you are able to switch which classes are being used in your configuration without needed any coding change to your workflows. This can be useful during development as you test out different scenarios, and also help ease the pain of migrating production workflows when new technology is adopted.  

This is the basic information needed to work with components. Some components are more complex than others and may have additional items to consider. When working with a component please review its requirements in the [integration](integrations.md) documentation to see if anything else is needed. 

### Definitely Global Components 

lolpop specially handles two components that are *always* global: a logger and a notifier. The logger allows integrations to log information to a standard location (such as a file) or service, and a notifier is meant to raise alerts during the running of a workflow that you'd like to know before the entire workflow completes (such as raising a notification via slack or email). Users can specify which logger and notifier to use in their configuration, but if none are provided, lolpop will load up the [StdOutLogger](stdout_logger.md) and [StdOutNotifier](stdout_notifier.md) for use in the workflow. These are subsequently passed to all other components and pipelines, and they are available to use via `self.log("message")` and `self.notify("message")`. 

### Likely Global Components 
A number of other components are likely to be global in many of your workflows, such as `metadata_tracker`, `metrics_tracker`, and `resource_version_control`. These tend to be so fundamental to so many other components that it can become difficult to design workflows without having components be dependent upon these. However, these are not forced global components because in a development setting you may wish to operate without the extra tooling. As you begin to progress your workflows into production, however, it is highly recommended to incorporate these. 

## Working with Pipelines 

In addition to configuration key-value pairs, pipeline configuration also contains local components. These components can only be accessed within the pipeline and by other components in the pipeline. 

```yaml title="Reference pipeline configuration" 
components: 
    component_type: ComponentClass
    ...
config: 
    key: value
    ... 

component_type: 
    <component_config>
...
```

Configuration can be accessed via `self._get_config("config_value")` and components can be accessed via `self.component_type`, just like they are in components. Note that `self._get_config()` will only retrieve configuration values from the pipeline and runner. If you wish to access a component's configuration, you can do so via `self.component_type._get_config()`.

Pipelines are independent, meaning that there is no built-in way to access one pipeline from another pipeline. If you wish to share information between pipelines, that should be handled at the runner level. 

Pipelines can be directly built from a pipeline class, but it's more common to built them as part of a runner. 

Note that pipeline type names are completely customizable by users, just like component type names. 

## Working with Runners 

Runners are the top level integration and likely the one which will be used the most. 

```yaml title="Reference runner configuration"
pipelines: 
    pipeline_type: PipelineClass
    ... 
components: 
    component_type: ComponentClass
    ...
config: 
    key: value
    ... 

pipeline_type: 
    <pipleine_config>

...

component_type: 
    <component_config>
...
```

Once a runner class is instantiated, runner configuration is accessible via `self._get_config()` and pipelines are accessible via `self.pipeline_type`. Global components can be accessed via `self.component_type` and pipeline local components can be accessed via `self.pipeline_type.component_type`. 

Runners can be built directly in python, or via the lolpop CLI. 

=== "Python"
    ```python 
    from lolpop.extensions import MyRunner

    config_file = "/path/to/dev.yaml"

    runner = MyRunner(conf=config_file)

    ...

    model = runner.train.train_model(data)

    ... 
    ``` 

=== "CLI"
    ```bash
    lolpop run workflow MyRunner --config-file /path/to/dev.yaml
    ```