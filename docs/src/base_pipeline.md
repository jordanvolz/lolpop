## Overview

Every pipeline should inherit from `BasePipeline`, either directly or indirectly (via inheriting from a pipeline that is built upon `BasePipeline`). The `__init__` function sets up the pipeline properly. If your pipeline needs to override `__init__` to include its own setup code, it is highly recommended to invoke the parent class' `__init__` via `super().__init__(*args, **kwargs)` as the first line of your own `__init__`. 

In production workflows, pipelines should be built automatically runners, and users should not need to explicitly create pipelines. For testing or development purposes, you may find a need to build a specific pipeline. The base pipeline anticipates the following arguments when constructing a pipeline: 

1. `conf` (dict): The pipeline configuration

2.  `runner_conf` (dict): The parent runner configuration

3. `parent_process` (str): The direct parent process of the pipeline (i.e the runner). 

4. `problem_type` (str): The ML problem type. I.E. `regression`, `classification`, etc. This is typically set at the runner level and passed down to all components. 

5. `pipeline_type` (str): The kind of pipline. I.E. `training`, `prediction`, etc. 

6. `components` (dict): Global components. This will be registered as attributes to the pipeline so that they can directly be accessed from within the pipeline.  

7. `skip_config_validation` (bool): Whether or not to skip configuration validation. Defaults to `False`.

## Interface

The `BasePipeline` implements the following methods, which will be available to all inheriting classes unless they are explicitly overwritten. 

### log 

Logs a message to the global logger component. 

```python
def log(self, msg, level="INFO", *args, **kwargs)
```

**Arguments**: 

- `msg` (str): The message to log. 

- `level` (str): The log level to use. 

### notify 

Sends a message to the global notifier component. 

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