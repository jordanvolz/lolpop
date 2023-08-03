# OfflineDeploy

The `OfflineDeploy` class is a subclass of the `BaseDeploy` class. It provides methods for promoting, checking approval, approving, and deploying models in an offline mode.

## Configuration 

### Required Configuration 

`OfflineDeploy` requires the following component types: 

- `metadata_tracker`
- `model_repository`
- `model_deployer`
- `resource_version_control`

## Methods

### promote_model 
Promotes a model to the model repository.

```python 
def promote_model(self, model_version, model=None, *args, **kwargs)
```


**Arguments**: 

- `model_version` (object): The version of the model to be promoted.
- `model` (object): The model object to be promoted (Optional).

**Returns**: 

- `promotion` (object): The promotion object that contains information about the promoted model.


### check_approval 

Checks if the given model promotion is approved in the model repository.


```python 
def check_approval(self, promotion, *args, **kwargs)
```


**Arguments**: 

- `promotion` (object): The promotion object that contains information about the promoted model.


**Returns**: 

- `is_approved` (bool): True if the promotion is approved, False otherwise.



### approve_model 

Approves the given model promotion in the model repository.


```python 
approve_model(self, promotion, *args, **kwargs)
```


**Arguments**: 

- `promotion` (object): The promotion object that contains information about the promoted model.

**Returns**: 

- `approval` (object): The approval object that contains information about the approved model promotion.



### deploy_model 
Deploys the given model promotion.

```python 
deploy_model(self, promotion, model_version, *args, **kwargs)
```



**Arguments**: 

- `promotion` (object): The promotion object that contains information about the promoted model.
- `model_version` (int): The version of the model to be deployed.

**Returns**: 

- `deployment` (object): An object that contains information about the deployed model.
