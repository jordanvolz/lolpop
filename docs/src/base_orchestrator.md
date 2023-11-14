## Overview

A `orchestrator` is a component that runs, tracks, and monitors workflows.  Although lolpop is capable of running workflows, either by itself or via some pipeline integration, it doesn't natively support tracking or monitoring of workflows. This is where an external orchestrator can be valuable. 

## Attributes

`BaseOrchestrator` contains no default attributes. 

## Configuration

`BaseOrchestrator` contains no required components or configuration.
 
## Interface

The following methods are part of `BaseOrchestrator` and should be implemented in any class that inherits from this base class: 

### decorator

Most modern python orchestration tools track execution of workflows via decorators. The decorator method here acts as an entrypoint for lolpop to properly decorate its own classes with the orchestrator's decorator. Typically, this is not called directly, but applied internally by lolpop. 

```python
def decorator(self, func, cls) -> Any:
```

**Arguments**: 

- `func` (object): The function to decorate.
- `cls` (object): The class containing the function.

**Returns**:

The decorated function.


### package 
Packages a lolpop class to be execute by the orchestrator. It's expected that calling this function produces something like a docker image, which can then be run by the orchestrator. 

```python 
def package(self, lolpop_class, lolpop_module, lolpop_entrypoint, *args, **kwargs) -> None:
```

**Arguments**:

  - `lolpop_class` (str): Name of the lolpop class to package.
  - `lolpop_module` (str): Name of the lolpop module to package.
  - `lolpop_entrypoint` (str): Name of the lolpop entrypoint to package.

**Returns**:

  - None


### deploy 
Deploys the packaged lolpop entrypoint into the orchestrator. The result of calling this function should mean that the orchestrator can now run the workflow.

```python 
def deploy(self, deployment_name, *args, **kwargs) -> None:
```


**Arguments**:

  - `deployment_name` (str): Name of the deployment to create.

**Returns**
  - None


### run 
Runs a lolpop workflow via the orchestrator.

```python 
def run(self, deployment_name, *args, **kwargs) -> tuple[str, str]:
```


**Arguments**:

- `deployment_name` (str): The deployment name to run.

**Returns**

- (id, url): A tuple containing the ID of the workflow instance and a URL to view that instance.


### stop 
Shuts down a current deployment.

```python
def stop(self, deployment_name, *args, **kwargs) -> None:
```

**Arguments**:

- `deployment_name` (str): The deployment name to shut down.


**Returns**:
None