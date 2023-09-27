Configuration is a large part of the lolpop experience. Components, pipelines, and runners should all be designed in a generic manner and expose specific decisions via configuration. I.E. when designing an integration, try to avoid using any hard-coded values and instead opt to allow users to customize behavior via configuration. You should also anticipate what pieces of your integration will need to be flexible and defined at runtime by the user. 

We would expect that almost every integration would allow some sort of configuration. For example, a model trainer should allow users to specify parameters to pass into the model training library, a data connector should allow users to specify the location of the data, a model training pipeline should specify which metric to optimize for, etc. 

Designing your workflows in this way makes it easy to reuse components as you can achieve different functionality by a simple configuration change instead of relying on code changes. 

## Configuration Overview

Configuration can be provided to lolpop in one of two ways: either via a `yaml` file or via a python dictionary. The former is recommended for production workflows. `yaml` files should be created for production work and can easily be tracked and versioned in your version control system of choice. `yaml` files can sometimes be clumsy to work with during development, so lolpop also supports using python dictionaries of configuration, which allows users to more easily change configuration on the fly. 

While initializing a component, pipeline, or runner, users can provide configuration via the `conf` parameter. This can either be a string containing a path to a `yaml` file or a python dictionary of configuration values. So, both of the following are valid: 

```yaml title="my_conf.yaml"
pipelines: 
    process : MyProcessPipeline 
    train : MyTrainingPipeline
    predict : MyPredictionPipeline
components: 
    metadata_tracker : MLFlowMetadataTracker
config: 
    train_data: /path/to/train.csv
    eval_data: /path/to/test.csv
```

```python title="YAML-based configuration"
config_file = "/path/to/my_conf.yaml"
runner = MyRunner(conf=config_file)
```

```python title="Dictionary-based configuration"
config = {
    "pipelines": {
        "process" : "MyProcessPipeline", 
        "train" : "MyTrainingPipeline", 
        "predict" : "MyPredictionPipeline",
    },
    "components": {
        "metadata_tracker" : "MLFlowMetadataTracker",
    }
    "config": {
        "train_data": "/path/to/train.csv",
        "eval_data": "/path/to/test.csv",
    }
}
runner = MyRunner(conf=config)
```

Configurations can stack with dependent integrations. I.E. your runner configuration can (and probably *should*) also contain the configuration for all pipelines and components that are going to be used in the worklow. lolpop knows how to parse the configuration accordingly and will instantiate every dependent integration with the corresponding configuration. In this way, it's simple to define your entire workflow configuration in one file or dictionary and allow lolpop to do the busy work of initializing all classes for you. 

Generally speaking, users will most often pass configuration directly into runners. Doing so allows the runners to build all dependent pipelines and components, and users need only maintain one configuration file/dictionary. However, for development/testing/debugging purposes you may find it useful to directly instantiate a pipeline or runner. This process is exactly the same, you need only provide just the configuration for the pipeline or component in question. 

Also note that configuration values from parents are available in all children. So, components know the configurations of the pipeline and runner that they are a part of, and pipelines know the configuration of runners. With this information, users should be able to easily specify configuration in one location and have it cascade down to whatever else needs it. 

### Configuration Linking

In some instances, you may have duplicate values used in your configuration. Having to remember to switch each value every time you wish to change it can be tedious, so lolpop allows you to link to other values in your configuration. You can do this via the following syntax `$path.to.config.value`. Here path to config value refers to the yaml or dictionary path to talk in order to get to that value. For example, let's consider a configuration where we wanted to reuse connection configuration for a `data_connector` between data processing and prediction pipelines: 

```yaml
...
process: 
    components: 
        data_connector: SnowflakeDataConnector
    data_connector: 
        config: 
            snowflake_account: my_account.snowflakecomputinc.com
            snoflake_user: DineshChugtai
            snowflake_password: GilfoyleIsMyBestFriend
            snowflake_database: dev
            snowflake_schema: training_data
            snowflake_warehouse: model_preproc
...
predict: 
    components: 
        data_connector: SnowflakeDataConnector
    data_connector: 
        config: 
            snowflake_account: $process.data_connector.config.snowflake_account
            snoflake_user: $process.data_connector.config.snowflake_user
            snowflake_password: $process.data_connector.config.snowflake_password
            snowflake_database: prod
            snowflake_schema: prediction_data
            snowflake_warehouse: $process.data_connector.config.snowflake_warehouse
...
```

!!! note 
    We would recommend against storing user credentials in your configuration. More on this later. 

In the above, the `predict` pipeline configuration reuses configuration values from the `process` pipeline, so when a change is made in the future to the `process` pipeline, the `prediction` pipeline will automatically pick it up as well. 

## Required and Default Configuration

lolpop has a couple of additional concepts with regards to configurations which helps integration designers guide people to using their integrations in the right way. In this section we'll discuss *required* and *default* configurations.

Each and every integration has attributes for required configuration `__REQUIRED_CONF__` and default configuration `__DEFAULT_CONF__`. This allows developers to specify which configurations users are expected to supply when using the integration, as well as pre-populating default configurations for things that users might not necessarily need or want to specify. For example, if I'm designing a new model trainer for an external library, I might include default model parameters which should provide fairly good performance on a wide array of problems. If users are experts in the library, they can then override the defaults when specifying the component configuration to try different values. This process of required and default configurations aims to give users a lot of freedom when executing workflows while still allowing developers to provide a guiding hand. 

### Syntax for Required Configuration 

Required configuration takes the following form: 

```python
__REQUIRED_CONF__ = {
    "pipelines": ["RequiredPipeline1", "RequiredPipeline2",...]
    "components": ["RequiredComponent1", "RequiredComponent2",...]
    "config": ["RequiredConfig1", "RequiredConfig2",...]
}
```

As seen above, required configuration is a dictionary where each item is a list of required integrations, except for `config`, which is just a list of required configuration values. For integrations, you should list the generic name of the integration and not the class name. I.E. use `metadata_tracker` and **not** `MLFlowMetadataTracker`. When building your own integrations, you may wish to specify that whatever you are building not only relies on a certain type of integration, but you only anticipate it working with a specific class. In these instances you can further specify your requirements limited to a specific class via `RequiredComponent|AcceptableClass1,AcceptableClass2,...`. This instructs lolpop to further consider only classes contained left of the `|` as valid when validating the integration's configuration.   

If you're designing your own integration, it's best practice to include in your require configuration any other integration that is used in that code, as well as any configuration values that are accessed. 

### Syntax for Default Configuration 

Default configuration takes the following form:

```python
__DEFAULT_CONF__ = {
    "config": {
        "key1": "value1", 
        "key2": "value2",
    }
}
```

Here, we simply provide a dictionary of key-value pairs to the component to use as a set of default configuration. 

## Configuration Validation

One of the great advantages of using required configuration is that lolpop is able to look at incoming configuration to an integration and compare it to the required configuration and figure out if something is missing. If so, lolpop will short-circuit the workflow. The assumption here is that if required configuration is missing then the workflow will fail further down the line. 

When performing validation, lolpop looks for configuration values in the following places: 

1. The passed in configuration for the integration. 
2. The configuration for parent integrations. 
3. The default configuration for the integration.

If a required configuration is not found in any of these places, lolpop will raise an error while loading the integration and specify which configuration values are missing. 

### Disabling Configuration Validation

We don't recommend disable configuration validation for production workflows. During development, you can disable configuration validation by adding the parameter `skip_config_validation=True` when you instantiate your integration. 

## Accessing Configuration

Accessing configuration values in lolpop is quite easy. Assuming your integrations are inheriting from `BaseComponent`, `BasePipeline`, or `BaseRunner`, they will inherit the method `_get_config("config_value", <default_value>)`. This method takes the configuration value to look for and an optional default value to return if none is found. lolpop searches for the value in the following places: 

1. The provided configuration for the integration 
2. The configuration for any parents of the integration 
3. The default configuration of the integration
4. Environment variables

Accessing configuration via environment variables is a last ditch effort meant to provide some current support for CI/CD-style workflows. In the future we anticipate having built-in support for secret managers. 

## YAML Configuration Reference

A `YAML` configuration file will likely contain runner, pipeline, and component configuration. Each follows a similar pattern, as seen below. 

=== "Runner" 
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
=== "Pipeline" 
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
=== "Component" 
    ```yaml title="Reference component configuration"
    config: 
        key: value
        ... 
    ```

Each integration manages its own configuration, so please reference the relevant [integration](integrations.md) documentation to see what values are expected. 

## Dictionary Configuration Reference

The dictionary structure follows along with the `yaml` structure shown above. In particluar: 

=== "Runner" 

    ```python title="Reference runner configuration"
    config = {
        "pipelines": {
            "pipleine_type" : "pipeline_class", 
            ...
        },
        "components": {
            "component_type" : "component_class",
            ...
        }
        "config": {
            "key": "value",
            ...
        }
        "pipeline_type" : {
            <pipeline_configuration>
        }
        "compoennt_type": {
            <component_configuration>
        }
    }
    ```
=== "Pipeline" 

    ```python title="Reference pipeline configuration"
    config = {
        "components": {
            "component_type" : "component_class",
            ...
        }
        "config": {
            "key": "value",
            ...
        }
        "compoennt_type": {
            <component_configuration>
        }
    }
    ```
=== "Component" 
    ```python title="Reference component configuration"
    config = {
        "config": {
            "key": "value",
            ...
        }
    }
    ```