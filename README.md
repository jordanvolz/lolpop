# lolpop
A software engineering framework forto jumpstart your MLOps projects

## install 

Install lolpop by cd'ing to the this directory and executing: 

```
pip install -e .
``` 

## running 

Try out the classification example in `examples`. To run it, simply execute

```
python examples/classification/mlrunner.py 
```
Note: You'll want to update `examples/classification/main_local.yaml` with your own snowflake & dbt config. 

## contributing 

If you're interested in contributing, there is a basic CLI tool that can boostrap a new runner/pipeline/component for you. 
To use, simply execute: 

```
python cli/cli.py create component <component_type> <componenet_class>
```

Component type should be one of component, pipeline, or runner. This will create a new component type in the specified directory in lolpop.  


