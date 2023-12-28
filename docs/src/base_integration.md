## Overview

Every integration should inherit from `BaseIntegration`, either directly or indirectly (via inheriting from a integration that is built upon `BaseIntegration`, such as `Baseintegrations`, `BasePipeline`, and `BaseRunner`). The `__init__` function sets up the integraiton properly. If your integration needs to override `__init__` to include its own setup code, it is highly recommended to invoke the parent class' `__init__` via `super().__init__(*args, **kwargs)` as the first line of your own `__init__`. 

In production workflows, integrations should be built automatically from configurations (either via `yaml` or a `dic t` provided programatically), and users should not need to explicitly create integrations. For testing or development purposes, you may find a need to build a specific integration. The base integrations anticipates the following arguments when constructing a integrations: 



1. `conf` (`dict` | `str`): The integrations configuration. Can be either a string (local file path to `yaml` file) or a dictionary of [configuration](configuration.md) 

2. `parent` (`obj` | `None`): The parent integration. This is typically not provided by users and is used by lolpop while recursively building your workflow. Defaults to None.

3.  `integration_type` (`str` | `None`): The name of the integration type. Defaults to None and lolpop will attempt to populate this from the module. 

4. `integration_framework` (`Anytree` | `None`): The `anytree` object representing the framework used by this component. This defaults to `None` and is not intended to be supplied by users. lolpop will pass this while recursively building the workflow and users are simply meant to provide an [integration_framework](integration_framework.md) in their workflow configuration, or use the built-in default of runner, pipelines, and components. 

5. `problem_type` (`str`): The ML problem type. I.E. `regression`, `classification`, etc. This is typically set at the runner level and passed down to all integrations. 

6. `dependent_integrations` (`dict`): Dependent integrations. All integrations here will be registered as child attributes to the integration so that they can directly be accessed from within the integration. This is meant to be populated by lolpop while recursively building the workflow. 

7. `skip_config_validation` (bool): Whether or not to skip configuration validation. Defaults to `False`.

8. `decorators` (`list`): A list of [decorators](using_custom_decorators.md) to apply to the workflow. This should not be directly supplied by users, but should be populated by lolpop based on a the `decorator` section of the workflow configuration and provided by lolpop while building the workflow recursively.

9. `is_standalone` (`bool`): Defaults to `False`. Used to specify that a component is not part of a workflow. This causes lolpop to skip processing an integration's integration framework. This is typically used if an integration is to be dynamically loaded during a workflow, and not as part of the integration framework. 


## Interface

The `BaseIntegration` implements the following methods, which will be available to all inheriting classes unless they are explicitly overwritten. 

### log 

Logs a message to the global logger integration. 

```python
def log(self, msg, level="INFO", *args, **kwargs)
```

**Arguments**: 

- `msg` (str): The message to log. 

- `level` (str): The log level to use. 

### notify 

Sends a message to the global notifier integration. 

```python
def notify(self, msg, level="ERROR", *args, **kwargs)
```
**Arguments**: 

- `msg` (str): The message to log. 

- `level` (str): The log level to use. 

### _get_config

Retrieve a configuration value. 

```python 
def _get_config(self, key, default_value=None)
```

**Arguments**: 

- `key` (str): The key to look up. 

- `default_value` (Any): The default value to return if the key is not found.

### _set_config

Set a configuration value. 

```python
def _set_config(self, key, value)
```

**Arguments**: 

- `key` (str): The key to use. 

- `value` (Any): The value to use.

### _validate_conf

Validates that the provided configuration for an integration satisfies the required configuration specified by the integration. 

```python
def _validate_conf(self, conf, dependent_integrations)
```

**Arguments**: 

- `conf` (dict): The configuration object. Should be already processed by lolpo. 

- `dependent_integrations` (dict): The dictionary of dependent integrations passed into the object during instantiation. lolpop will check to see if any missing integrations are provided in the dependent_integrations object. 


### _update_integrations

Sets all provided integrations to be attributes to this object. 

```python
def _update_integrations(self, integrations, *args, **kwargs)
```

**Arguments**: 

- `integrations` (dict): dictionary of integrations to set into this object. Should be of the form `"attribute_name" : object`

### _print_integrations

Prints all integrations attached to this object. 

```python
def _print_integrations_(self)
```

**Arguments**: 

None

**Sample Output**: 

```sh
>>> int._print_integrations()
Integrations attached to runner MyRunner:

 component
 -- data_checker (EvidentlyAIDataChecker)
 -- logger (StdOutLogger)
 -- metadata_tracker (MLFlowMetadataTracker)
 -- metrics_tracker (MLFlowMetricsTracker)
 -- notifier (StdOutNotifier)

  pipeline
 -- train (OfflineTrain)
```

### _print_integration_framework()

Prints an object's integration framework.

```python
def _print_integration_framework(self)
```

**Arguments**: 

None

**Sample Output:**

```sh
>>> int._print_integration_framework( )
AnyNode(id='runner')
├── AnyNode(id='component')
└── AnyNode(id='pipeline')
    └── AnyNode(id='component')
```