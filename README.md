# lolpop
A software engineering framework to jumpstart your Machine Learning projects

## install 

You can install lolpop from pip: 

```bash
pip install lolpop
```

If you're working in dev mode, you can clone this repo and install lolpop by cd'ing to the this directory and executing: 

```bash
poetry install 
pip install -e .
``` 

Note: getting the poetry install to work has been difficult, due to some of conflicts among packages (I think primarly `dbt`. If you're having issues getting it to work, feel free to try removing things that are troublesome and/or moving it into a requirements.txt file and installing via `pip`)

## running 

Try out the classification example in `examples/classification/mlflow`. To run it, simply execute

```bash
python3 examples/classification/mlflow/mlrunner.py 
```
Note: You'll want to update `examples/classification/mlflow/local_dev.yaml` with your own configuration. In particular, update the mlflow configuration. You also need to download the `test.csv` and `train.csv` files 
from [Kaggle](https://www.kaggle.com/competitions/petfinder-adoption-prediction/data) and update your conf to point to their locations. 

You'll probably hit a few errors in trying to run the first time. Let me know what they are. 

## contributing 

If you're interested in contributing, there is a basic CLI tool that can boostrap a new runner/pipeline/component for you. 
To use, simply execute: 

```bash
python3 cli/cli.py create component/pipeline/runner <component_type> <component_class>
```

Component type should be something like metadata_tracker, metrics_tracker, model_trainer, etc, and component class is the name of the class. This will create a new component type in the specified directory in lolpop.  
This will boostrap a cookiecutter project in the provided `--component-dir` which you can then edit as desired. 


