## Overview

The `deploy` pipeline is a pipeline that performs common actions concerning model deployments, such as promoting and approving model versions, as well as deploying model versions to end points. Typically we would expect the following chain for a production model: model built -> promotion (technical approval) -> approval (legal/compliance approval) -> deployment. 

## Attributes

`BaseDeploy` contains no default attributes. 

## Configuration

`BaseDeploy` contains no default or required configuration. 


## Interface

The following methods are part of `BaseDeploy` and should be implemented in any class that inherits from this base class: 

### promote_model

Promotes a model version. 

```python
def promote_model(self, model_version, *args, **kwargs) -> Any
```

**Arguments**: 

- `model_version` (object): The model version object that is being promoted.  

**Returns**:

- `promotion` (object): Returns a promotion object, very likely returned back from a `model_respository`. 


### approve_model

Approves a promotion (i.e. model version). 

```python
def approve_model(self, promotion, *args, **kwargs) -> Any
```

**Arguments**: 

- `promotion` (object): The promotion to approve.  

**Returns**:

- `approval` (object): Returns an approval object, very likely returned back from a `model_respository`. 

### deploy_model

Creates a deployment of an approved model version. 

```python
def deploy_model(self, promotion, *args, **kwargs) -> Any
```

**Arguments**: 

- `promotion` (object): The promotion to deploy

**Returns**:

- `deployment` (object): Returns a deployment object, very likely returned back from a `model_deployer`. 

### check_approval

Creates a deployment of an approved model version. 

```python
def check_approval(self, promotion, *args, **kwargs) -> bool
```

**Arguments**: 

- `promotion` (object): The promotion to check to see if it has been approved. 

**Returns**:

- `bool` (object): Whether the promotion is approved or not. 

