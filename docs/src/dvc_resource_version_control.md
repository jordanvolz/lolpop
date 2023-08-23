# dvcVersionControl

The `dvcVersionControl` class is a subclass of `BaseResourceVersionControl` and provides methods for versioning datasets and models using Data Version Control (DVC). It is used to manage the versioning of resources in a machine learning or data science project.

## Configuration 

### Required Configuration
`dvcVersionControl` contains no required configuration. 

### Optional Configuration 
`dvcVersionControl` contains no default configuration. 

### Default Configuration 

`dvcVersionControl` contains no default configuration. 

- `dvc_remote`: the dvc remote to use, defaults to `local`
- `dvc_dir`: the directory corresponding to the dvc directory, defaults to `dvc/`
- `local_dir`: a local directory
- `disable_git_commit`: Disable all git commits in the workflow. This is meant to be used only in development/test settings. Defaults to False.
- `disable_git_push`:  Disable all git pushes in the workflow. This is meant ot be used only in development/test settings. Defaults to False. 
- `git_path_to_dvc_dir`: The path to the dvc directory relative to the git repository. This is needed if you execute `dvc init --subdir` such that the dvc repo and the git repo are not at the same level. This is mainly intended to be used for testing purposes. Defaults to `None`.  

!!! Note
    The `dvcVersionControl` component assumes that the lolpop workflow is running from a git repository and that a subfolder is used to designate the dvc artifacts. User should configure which folder to use for the `dvc_dir` and the `dvc_remote` to use. If no dvc_remote is configured, lolpop will attempt to use dvc in local mode, which saves objects to a directory in your local file system. By default this wil be configured to be `local_dir`/dvc

## Methods

### version_data 
This method versions the input dataset using DVC and outputs information about the versioned dataset, including the versioning ID and URI.

```python
def version_data(self, dataset_version, data, key=None, *args, **kwargs)
```

**Arguments**:

- `dataset_version`: (object), dataset version object to version
- `data`: (DataFrame), the dataset to version
- `key`: (str), optional, default: None, a unique identifier for the dataset version


**Returns**: 

A dictionary containing dataset versioning information including the URI and hexsha.


### get_data 
This method retrieves the versioned dataset from DVC using information about the dataset version.

```python 
def get_data(self, dataset_version, vc_info=None, key=None, *args, **kwargs)
```

**Arguments**: 

- `dataset_version`: (object) dataset version object
- `vc_info`: (dictionary), optional, containing versioning information for the dataset
- `key`: (str), optional, default: None, a unique identifier for the dataset version

**Returns**: 

A DataFrame containing the versioned dataset.


### version_model 
This method versions the input model using DVC and outputs information about the versioned model, including the versioning ID and URI.


```python 
def version_model(self, experiment, model, algo=None, key=None, *args, **kwargs)
```

**Arguments**: 

- `experiment`: (object), experiment object being versioned
- `model`: (object), the model to version
- `algo`: (str), the algorithm used to train the model
- `key`: (str), optional, default: None, a unique identifier for the model version


**Returns**:

A dictionary containing model versioning information including the URI and hexsha.

### get_model 
This method retrieves the versioned model using versioning information about the model.


```python
def get_model(self, experiment, key=None, args, kwargs)
```

**Arguments**: 

- `experiment`: (object), experiment whose model we are retrieving
- `key`: (str), optional, default: None, a unique identifier for the model version

**Returns**: 
The versioned model.


## Usage 

```python
from lolpop.component import dvcVersionControl

... # create data and dataset_version 

config = {
    #insert component config
}

rvc = dvcVersionControl(conf=config)

vc_info = rvc.version_data(dataset_version, data)

df = rvc.get_data(dataset_verion, vc_info=vc_info)
```

