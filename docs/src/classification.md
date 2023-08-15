
This guide will walk us through a quick example of predicting the time to adoption for pets on the popular website [Petfinder](https://petfinder.com). 

## Setup

1. First, let's create a virtual environment for this example: 

    ```bash
    python3 -m venv ~/venv/petfinder
    ```
    Feel free to replace `~/venv/petfinder` with any path where you'd like to store the virtual environment. 

    Now, activate the  virtual environment: 

    ```bash
    source ~/venv/petfinder/bin/activate
    ```

2. Now let's install the packages we'll need for this example: 

    ```bash 
    pip3 install 'lolop[cli,mlflow,xgboost,dvc,evidently,deepchecks,optuna,yellowbrick,aif360,alibi]'
    ```

3. This example will version data with dvc. In order to use it, we'll need a git repo to use with dvc. For the purposes of this guide, we'll create a git repository in our provider of choice named `lolpop_petfinder_example`. You'll then want to clone this repo locally via something like: 

    ```bash 
    git clone git@github.com:jordanvolz/lolpop_petfinder_example.git
    ```

    Now let's clone the `lolpop` repository to get the files we need for our example. 

    ```bash
    git clone git@github.com:jordanvolz/lolpop.git
    ```

    And then we'll move the petfinder example files into our new repository: 

    ```bash
    cp -r lolpop/examples/classification/petfinder/* lolpop_petfinder_example
    ```

    Now, we'll move into the `lolpop_petfinder_example` directory and set up dvc: 

    ```bash 
    cd lolpop_petfinder_example 
    mkdir dvc
    dvc init 
    mkdir /tmp/artifacts
    dvc remote add -d local /tmp/artifacts
    ```

    Note: if you already use dvc, feel free to use a different remote. In this example, we're simply using the local directory `/tmp/artifacts` to store our dvc artifacts. If you use a different remote than local, you'll need to configure that in the `dev.yaml` file to point to the correct remote for the [dvcVersionControl](dvc_resource_version_control.md) class. 

4. Now we'll download the data for the example from Kaggle. If you already use kaggle from the command line you can simply execute the following: 

    ```bash
    kaggle competitions download -c petfinder-adoption-prediction
    unzip -j -o petfinder-adoption-prediction.zip train/train.csv test/test.csv -d data

    ```
    Or, Manually download the data from the following [link](https://www.kaggle.com/competitions/petfinder-adoption-prediction/data) and unzip it. You should now have a `train.csv` and `test.csv` file in the `lolpop_petfinder_example/data` directory. 

## Running the Workflow 

1. To run our workflow, we'll simply need to execute the following command: 

    ```bash 
    python3 run.py 
    ```

2. You should see a bunch of `INFO` messages generated in your terminal. After several minutes your workflow should be finished. The end of your output will look something like: 

    ```bash 
    ...
    2023/08/13 20:52:40.363664 [INFO] <DeepchecksDataChecker> ::: DeepchecksDataChecker had 2 passed checks.
    2023/08/13 20:52:40.363811 [INFO] <DeepchecksDataChecker> ::: DeepchecksDataChecker had 6 failed checks.
    2023/08/13 20:52:40.363932 [INFO] <DeepchecksDataChecker> ::: DeepchecksDataChecker had 3 checks not run.
    2023/08/13 20:52:40.370277 [INFO] <MLFlowMetadataTracker> ::: Saving artifact /tmp/artifacts//DEEPCHECKS_DATA_REPORT.HTML.html to directory petfinder_adoption_speed_predictions_prediction_checks_report in artifact directory in run e2b197fc40124f2db32b6b2737337bc1
    Issues found with data checks. Visit ./mlruns for more information.
    2023/08/13 20:52:40.370758 [ERROR] <OfflinePredict> ::: Notification Sent: Issues found with data checks. Visit ./mlruns for more information.
    2023/08/13 20:52:40.541118 [INFO] <LocalDataConnector> ::: Successfully saved data to data/predictions.csv.
    2023/08/13 20:52:40.551292 [INFO] <dvcVersionControl> ::: Executing command: `dvc get git@github.com:jordanvolz/lolpop_petfinder_example.git dvc/petfinder_adoption_speed_predictions.csv --rev 9bb722ba3e9e3128dd0404bd9f4439fe2eaeb7e3 -o petfinder_adoption_speed_predictions.csv`
    2023/08/13 20:52:47.856724 [INFO] <LocalDataConnector> ::: Successfully loaded data from data/train.csv into DataFrame.                                                                                                             
    Current training data has no overlap with the prediction job petfinder_adoption_speed_predictions
    2023/08/13 20:52:48.088906 [WARNING] <ClassificationRunner> ::: Notification Sent: Current training data has no overlap with the prediction job petfinder_adoption_speed_predictions
    exiting...
    ```

## Exploring the Example 

1. This example uses MLFlow as your metadata tracker, which tracks all the artifacts we're creating. To view them, simply launch MLflow locally: 

    ```bash 
    mlflow ui
    ```

2. You can then open up your web browser and navigate to `http://localhost:5000`. You'll notice an experiment named `petfinder_adoption_speed` with a recently completed run. Feel free to dig around and look at what information got logged. 

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
