
Once lolpop is [installed](installation.md), we can begin building and running our ML workflows. 

## Running a Quickstart

To begin getting acquainted with the framework, lolpop comes with many examples. There are several "quickstart" examples which are designed to get users up and running as quickly as possible. These do not require any external accounts or connections in order to run, as all of the components leverage local compute resources during execution. This is a great first experience to get your feet wet and to begin to get a feel for lolpop's internals while minimizing additional setup required. 

1. [Install](installation.md) lolpop. 
  ```python
  pip3 install lolpop[cli,mlflow,xgboost]
  ```

2. Download the titanic dataset from [Kaggle](https://www.kaggle.com/competitions/titanic/data). Unzip the file and note the location of the `test.csv` and `train.csv` files. 

3. Clone the lolpop repo. 
  ```bash
  git clone git@github.com:jordanvolz/lolpop.git
  ```

4. Navigate to the `lolpop/examples/quickstart` folder and modify `quickstart.yaml` as follows: 

    a. Update the files paths of `train.csv`, `test.csv` and `predictions.csv` in `config.train_data`, `config.test_data`, and `config.prediction-data`, respectively. Note that the file path in `config.prediction_data` was not provided by the Kaggle dataset. This is because this is a file that lolpop will create. 
      ```yaml title="quickstart.yaml" hl_lines="4-6"
      ...

      config: 
        train_data: /path/to/train.csv
        eval_data: /path/to/test.csv
        prediction_data: /path/to/predictions.csv

      ...
      ```

    b. `config.local_dir` is a local scratch location that lolpop uses to save local artifacts. This is set to `/tmp/artifacts` by default, but feel free to switch this to another location, or, alternatively, ensure that `/tmp/artifacts` does exist. 
      ```yaml title="quickstart.yaml" hl_lines="3"
      config: 
        ...
        local_dir: /tmp/artifacts/

      ...
      ```
    
    c. In `process.data_transformer.transformer_path` update the value here to the location of `process_titantic.py`. In the lolpop github repo. 
      ```yaml title="quickstart.yaml" hl_lines="8"
      ...

      process: 
        component: 
          data_transformer: LocalDataTransformer
        data_transformer: 
          config: 
            transformer_path: /path/to/lolpop/examples/quickstart/process_titanic.py
      ...
      ```
    
    d. Update `metadata_tracker.config.mlflow_tracking_uri` to point to your mlflow location. If you haven't previously used mlflow, then you can just point this to some empty directory on your filesystem.
      ```yaml title="quickstart.yaml" hl_lines="5"
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

  python3 run.py 
  ```
Your console will begin logging output of your workflow, you'll see lines like this: 
  ```bash
  2023/06/21 15:16:31.727982 [INFO] <QuickstartRunner> ::: Loaded class StdOutLogger into component logger
  2023/06/21 15:16:31.805406 [INFO] <MLFlowMetadataTracker> ::: Using MLFlow in experiment titanic_survival with run id: dd79d0724cda42b79fcf19f3ad0e28ca
  2023/06/21 15:16:31.805668 [INFO] <QuickstartRunner> ::: Loaded class MLFlowMetadataTracker into component metadata_tracker
  2023/06/21 15:16:31.813281 [INFO] <QuickstartRunner> ::: Loaded class StdOutNotifier into component notifier
  ```
And it should run pretty quickly and you'll see something like: 
  ```bash
  2023/06/21 15:16:32.517021 [DEBUG] <OfflinePredict> ::: Finished execution of get_predictions. Completed in 0.30754699999999957 seconds.
  2023/06/21 15:16:32.517180 [DEBUG] <QuickstartRunner> ::: Finished execution of predict_data. Completed in 0.49444599999999994 seconds.
  2023/06/21 15:16:32.517330 [DEBUG] <QuickstartRunner> ::: Starting execution of stop
  2023/06/21 15:16:32.517553 [DEBUG] <MLFlowMetadataTracker> ::: Starting execution of stop
  2023/06/21 15:16:32.525008 [DEBUG] <MLFlowMetadataTracker> ::: Finished execution of stop. Completed in 0.07348200000000205 seconds.
  2023/06/21 15:16:32.525219 [DEBUG] <QuickstartRunner> ::: Finished execution of stop. Completed in 0.07735699999999923 seconds.
  exiting...
  ```

## Understanding the workflow

To gain some understanding about what is happening, let's look into the `run.py` file. This is a small script that loads our runner and executes a workflow. 

The first thing that happens is we load our runner and instantiate it with our `quickstart.yaml` file. 

```python title="run.py"
from quickstart_runner import QuickstartRunner

#create runner from config
config_file = "quickstart.yaml"
runner = QuickstartRunner(conf=config_file, skip_config_validation=True)
...
``` 
Instead of using a built-in runner from lolpop, we're using a local runner that is contained in the example. It's perfectly normal and expected that you may mix built-in components with custom components. 

Once our runner has been instantiated, we can then start executing part of our workflows via the pipelines we specified in our configuration, like below:

```python title="run.py"
...
#run data processing
train_data = runner.process_data()
...
```

This will run the `process_data` method in our `QuickstartRunner` class. If you look into that, we'll find the following: 

```python title="quickstart_runner.py"
...
    def process_data(self, source="train"):
        #run data transformations and encodings
        source_data_name = self._get_config("%s_data" % source)
        # maybe better called get_training_data?
        data = self.process.transform_data(source_data_name)

        return data
...
```
In this method, we get the source_data_name from our runner config (i.e. `train_data` in `quickstart.yaml`) and then we pass that into `self.process.transform_data`. However, it might not be immediately clear what `self.process` is, actually, and how did this come into existance? This is one of the pipelines we specified in our configuration. Specifically, in `quickstart.yaml` we register the following pipelines: 

```yaml title="quickstart.yaml"
...
pipeline: 
  process: OfflineProcess 
  train: OfflineTrain
  predict: OfflinePredict
...
```

What lolpop does with this configuration is that it loads each class to the assigned attribute on the runner object. So, for example, the `OfflineProcess` class gets mapped to `runner.process`, `OfflineTrain` to `runner.train` and `OfflinePredict` to `runner.predict`. There are no limitations here to what you can name your pipelines, so feel free to name them whatever works best for you. 

With this knowledge, the following line hopefully makes sense: 

```python title="quickstart_runner.py"
...
data = self.process.transform_data(source_data_name)
...
```
This actually runs `transform_data` in `OfflineProcess`:

```python title="offline_process.py"
...
    def transform_data(self, source_data_name): 
        #transform data
        data_out = self.data_transformer.transform(source_data_name)

        return data_out
...
```

Here we see that this really just executes `self.data_transformer.transform`. And we might additionally wonder what is `data_transformer` and how did it get created? If we return back to `quickstart.yaml` and look at our `process` configuration, we'll see what we are telling lolpop to do with this pipeline: 

```yaml title="quickstart.yaml"
...
process: 
  component: 
    data_transformer: LocalDataTransformer
  data_transformer: 
    config: 
      transformer_path: /path/to/lolpop/examples/quickstart/process_titanic.py
...
```

And, we should notice that `LocalDataTransformer` is mapped to `data_transformer` in this pipeline. Additionally, we add a piece of configuration for this component that instructs lolpop where to find the path of the transformer script to use. 

So, our pipeline loads up our `LocalDataTransformer` component and executes `transform`: 

```python title="local_data_transformer.py"
...
def transform(self, input_data, *args, **kwargs):
        if isinstance(input_data,dict) or isinstance(input_data, dictconfig.DictConfig): 
            data = {k: self.data_connector.get_data(v) for k,v in input_data.items()}
        elif isinstance(input_data,str): 
            data = self.data_connector.get_data(input_data)
        else: 
            raise Exception("input_data not a valid type. Expecting dict or str. Found: %s" %str(type(input_data)))
        kwargs = self._get_config("transformer_kwargs",{})

        data_out = self._transform(data, **kwargs)

        return data_out
...
```

Since we're passing a string into this function, it will call `get_data` out of the data_connector component to retrieve data, then call `self._transform` on that data. In this [init](https://github.com/jordanvolz/lolpop/blob/main/lolpop/component/data_transformer/local_data_transformer.py#L17) method, we can see that `self._transform` is just the entry point into our transformer script which is defined in `transformer_path`, i.e. the `process_titanic.py` script. 

Similarly, we can trace through the rest of run.py. The next step is to train a model. The script calls the runner method `train_model`. This will in turn leverage the `OfflineTrain` pipeline, which will then use one or more components to train a model. 

```python title="run.py"
...
#train model
model, model_version = runner.train_model(train_data)
```

Lastly, we make a prediction. This uses the `OfflinePredict` pipeline, which will use one or more components. 
```python title="run.py"
...
#run prediction
eval_data = runner.process_data(source="eval")
data, _ = runner.predict_data(model, model_version, eval_data)
```

We then call `runner.stop`, which we can use to handle anything we want to do at the end of a workflow -- commit files, clean up directories, etc. 
```python title="run.py"
...
#exit
runner.stop()
print("exiting...")
```

And that's it! Hopefully this gave you some intuition on what's happen behind the scenes with lolpop. You can continue digging in with our User Guide or by stepping through some more rigorous [examples](examples.md).
