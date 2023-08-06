
## Installing lolpop

lolpop can be installed directly from PyPI via:  

```bash 
pip install lolpop 
```

lolpop maintains many extra packages that can be installed based on what you are using it for. We would also recommend installing the `cli` extra: 

```bash
pip install 'lolpop[cli]'
```

To see a list of all available extras, you can use the following cli command (after installing the lolpop cli above): 

```bash 
> lolpop list-extras
aif360
alibi
aws
cli
databricks
dbt-core
deepchecks
duckdb
dvc
evidently
google
metaflow
mlflow
optuna
prefect
redshift
scikit-learn
snowflake
sweetviz
timeseries
xgboost
ydata-profiling
yellowbrick
``` 
## Local Development

If you're running lolpop from source, you can leverage poetry to handle your install. In particular, 

```bash 
poetry install
``` 

will install whatever is current in `pyproject.toml`. And, if you are working on a particular component for which you have added an extra package for: 

```bash
poetry install -E <extra_name>
```

Or, to install all extras: 

```bash
poetry install --all-extras
``` 

See the poetry [docs](https://python-poetry.org/docs/pyproject/#extras) for more information on using poetry. 