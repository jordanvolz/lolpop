
Once lolpop is [installed](installation.md), we can begin building and running our ML workflows. 

To begin getting acquainted with the framework, lolpop comes with many examples. There are several "quickstart" examples which are designed to get users up and running as quickly as possible. These do not require any external accounts or connections in order to run, as all of the components leverage local compute resources during execution. This is a great first experience to get your feet wet and to begin to get a feel for lolpop's internals while minimizing additional setup required. 

1. [Install](installation.md) lolpop. 
```python
pip3 install lolpop[cli,mlflow,xgboost]
```

2. Download the titanic dataset from [Kaggle](https://www.kaggle.com/competitions/titanic/data). Unzip the file and note the location of the `test.csv` and `train.csv` files. 

3. Clone the lolpop repo. 
```bash
git clone https://github.com/jordanvolz/lolpop
``` 
 (Note: In the future we'll likely move examples into their own repository, but for now they are coupled w/ the lolpop source code.)

4. Navigate to the `lolpop/examples/quickstart` folder and modify `quickstart.yaml` as follows: 

    a. Update the files paths of `train.csv`, `test.csv` and `predictions.csv` in `config.train_data`, `config.test_data`, and `config.prediction-data`, respectively. Note that the file path in `config.prediction_data` was not provided by the Kaggle dataset. This is because this is a file that lolpop will create. 
```yaml
...

config: 
  train_data: /path/to/train.csv
  eval_data: /path/to/test.csv
  prediction_data: /path/to/predictions.csv

...
```

    b. `config.local_dir` is a local scratch location that lolpop uses to save local artifacts. This is set to `/tmp/artifacts` by default, but feel free to switch this to another location, or, alternatively, ensure that `/tmp/artifacts` does exist. 
```yaml
config: 
  ...
  local_dir: /tmp/artifacts/

...
```
    
    c. In `process.data_transformer.transformer_path` update the value here to the location of `process_titantic.py`. In the lolpop github repo. 
```yaml 
...

process: 
  components: 
    data_transformer: LocalDataTransformer
  data_transformer: 
    config: 
      transformer_path: /path/to/lolpop/examples/quickstart/process_titanic.py
...
```
    
    d. Update `metadata_tracker.config.mlflow_trackign_uri` to point to your mlflow location. If you haven't previously used mlflow, then you can just point this to some empty directory on your filesystem.
```yaml
...

metadata_tracker: 
  config: 
    mlflow_tracking_uri: file:///path/to//mlruns
    mlflow_experiment_name: titanic_survival

...
```

5. CD into `lolpop/examples/quickstart/` and run the workflow:
```bash
cd lolpop/examples/quickstart

python3 mlruner.py 
```