
This guide will walk us through a quick example of predicting survivors on the infamous [sinking of the Titanic](https://en.wikipedia.org/wiki/Sinking_of_the_Titanic). Pretend like you've never seen this example worked out before. 

Buckle up, throw on Gavin Bryars' [iconic soundtrack](https://philipjeck.bandcamp.com/album/the-sinking-of-the-titanic-1969), and enjoy the slow descent. Spoiler: [Leo doesn't make it out alive](https://www.youtube.com/watch?v=KV-apmpMe80). 

## Setup

1. First, let's create a virtual environment for this example: 

    ```bash
    python3 -m venv ~/venv/titanic
    ```
    Feel free to replace `~/venv/titanic` with any path where you'd like to store the virtual environment. 

    Now, activate the  virtual environment: 

    ```bash
    source ~/venv/titanic/bin/activate
    ```

2. Now let's install the packages we'll need for this example: 

    ```bash 
    pip3 install 'lolpop[cli,mlflow,xgboost]'
    ```

3. Now let's clone the `lolpop` repository to get the files we need for our example. 

    === "HTTPS"
        ```bash
        cd ~/Downloads 
        git clone https://github.com/jordanvolz/lolpop.git
        cd lolpop/examples/quickstart/classification/titanic
        ```
    === "SSH"
        ```bash
        cd ~/Downloads 
        git clone git@github.com:jordanvolz/lolpop.git
        cd lolpop/examples/quickstart/classification/titanic
        ```

4. Now we'll download the data for the example from Kaggle. If you already use kaggle from the command line you can simply execute the following: 

    ```bash
    kaggle competitions download -c titanic
    unzip titanic.zip
    ```
    !!! Note
        You'll need to accept the terms of the kaggle contest to be able to download the data. If you've not already done that, you may wish to just manually download the data from the link below. 

    Or, manually download the data from the following [link](https://www.kaggle.com/competitions/titanic/data) and unzip it. You should now have a `train.csv` and `test.csv` file in the `lolpop/examples/quickstart/classification/titanic` directory. 

## Running the Workflow 

1. To run our workflow, we'll simply need to execute the following command: 

    ```bash 
    python3 run.py 
    ```

2. You should see a bunch of `INFO` messages generated in your terminal. After a few seconds your workflow should be finished. The end of your output will look something like: 

    ```bash 
    ...
    2023/08/11 02:52:40.478907 [INFO] <MLFlowMetadataTracker> ::: Saving metadata key=model_trainer, value=XGBoostModelTrainer to run 3eba6becd94b46cf9281d77fa602cf0a
    2023/08/11 02:52:40.479475 [INFO] <MLFlowMetadataTracker> ::: Saving tag key=3eba6becd94b46cf9281d77fa602cf0a.titanic_survival.model_trainer, value=XGBoostModelTrainer to run 3eba6becd94b46cf9281d77fa602cf0a
    2023/08/11 02:52:40.602068 [INFO] <MLFlowMetadataTracker> ::: Saving metadata key=winning_experiment_id, value={'winning_experiment_id': '3eba6becd94b46cf9281d77fa602cf0a.titanic_survival'} to run 5539824a84ea43129ba04d003d51e8e4
    2023/08/11 02:52:40.602662 [INFO] <MLFlowMetadataTracker> ::: Saving tag key=titanic_survival.winning_experiment_id, value={'winning_experiment_id': '3eba6becd94b46cf9281d77fa602cf0a.titanic_survival'} to run 5539824a84ea43129ba04d003d51e8e4
    2023/08/11 02:52:40.604804 [INFO] <MLFlowMetadataTracker> ::: Saving metadata key=winning_experiment_model_trainer, value={'winning_experiment_model_trainer': 'XGBoostModelTrainer'} to run 5539824a84ea43129ba04d003d51e8e4
    2023/08/11 02:52:40.605447 [INFO] <MLFlowMetadataTracker> ::: Saving tag key=titanic_survival.winning_experiment_model_trainer, value={'winning_experiment_model_trainer': 'XGBoostModelTrainer'} to run 5539824a84ea43129ba04d003d51e8e4
    2023/08/11 02:52:40.613509 [INFO] <LocalDataConnector> ::: Successfully loaded data from test.csv into DataFrame.
    2023/08/11 02:52:40.618509 [INFO] <LocalDataConnector> ::: Successfully saved data to predictions.csv.
    exiting...
    ```

## Exploring the Example 

1. This example uses MLFlow as your metadata tracker, which tracks all the artifacts we're creating. To view them, simply launch MLflow locally: 

    ```bash 
    mlflow ui
    ```

2. You can then open up your web browser and navigate to `http://localhost:5000`. You'll notice an experiment named `titantic_survival` with a recently completed run. Feel free to dig around and look at what information got logged. Note: for the quickstart example, we've paired this down to the bare minimum, so there is not a ton to see here. The regular examples contain much more information. 

3. Predictions from the model get saved to `predictions.csv`. You can view them via: 

    ```bash
    cat predictions.csv
    ```

    Or in python via: 
    ```
    import pandas as pd 

    df = pd.read_csv("predictions.csv")
    df.head() 
    ```

## Understanding the Example

!!! Note
    The text here is exactly the same as the text in our [regression quickstart](regression.md#understanding-the-example) example. The reason being that both use the same quickstart_runner.py class. The only difference is the value of the `problem_type` set during initialization of the class. 

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

And that's it! Hopefully this gave you some intuition on what's happen behind the scenes with lolpop. You can continue digging in with our User Guide or by stepping through some more rigorous [examples](classification.md).
