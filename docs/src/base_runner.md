## BaseRunner

Every runner should inherit from `BaseRunner`,  The `__init__` function sets up the runner properly, as well as all child pipelines and components. If your component needs to override `__init__` to include its own setup code, it is highly recommended to invoke the parent class' `__init__` via `super().__init__(*args, **kwargs)` as the first line of your own `__init__`. 

In production workflows, components should be built automatically from pipeline and runners, and users should not need to explicitly create components. For testing or development purposes, you may find a need to build a specific component. The base component anticipates the following arguments when constructing a component: 

1. `conf` (dict): The runner configuration. 

2. `problem_type` (str): The ML problem type. I.E. `regression`, `classification`, etc. This will be passed down to all components. 

3. `skip_config_validation` (bool): Whether or not to skip configuration validation. Defaults to `False`.

## Interface

The `BaseRunner` implements the following methods, which will be available to all inheriting classes unless they are explicitly overwritten. 

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