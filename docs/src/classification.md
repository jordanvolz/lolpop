
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
    pip3 install 'lolpop[cli,mlflow,xgboost,dvc,evidently,deepchecks,optuna,yellowbrick,aif360,alibi]'
    ```

3. This example will version data with dvc. In order to use it, we'll need a git repo to use with dvc. For the purposes of this guide, we'll create a git repository in our provider of choice named `lolpop_petfinder_example`. You'll then want to clone this repo locally via something like: 

    === "HTTPS" 
        ```bash
        git clone https://github.com/<git_user>/lolpop_petfinder_example.git
        ```
    === "SSH"
        ```bash 
        git clone git@github.com:<git_user>/lolpop_petfinder_example.git
        ```

    Now let's clone the `lolpop` repository to get the files we need for our example. 

    === "HTTPS"
        ```bash
        git clone https://github.com/jordanvolz/lolpop.git
        ```
    === "SSH"
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
    !!! Note
        You'll need to accept the terms of the kaggle contest to be able to download the data. If you've not already done that, you may wish to just manually download the data from the link below. 

    Or, manually download the data from the following [link](https://www.kaggle.com/competitions/petfinder-adoption-prediction/data) and unzip it. You should now have a `train.csv` and `test.csv` file in the `lolpop_petfinder_example/data` directory. 

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

To get a feel for tracing through the runner, pipeline and component code, see the [quickstart](classification_quickstart.md) guide. This example follows the same principles, it just does much more. As a summary for what this workflow accomplishes: 

**Data Processing**: 

- Data is transformed via a `data_transformer` component. This would typically involve doing some light data engineering or feature engineering to get data into a single dataset. 

- Data is versioned and tracked using the `metadata_tracker` and the `resource_version_control`

- Data is profiled via a `data_profiler`. This performs an EDA style analysis of the data and save the output report. 

- Data is run through a series of data checks, via a `data_checker`. These checks are typically associated with data quality/integrity. Again, the output report should be saved into the `metadata_tracker`.

- Finally, the `data_profiler` fetches the previous data version and runs a data comparison report. The output report will be saved into the `metadata_tracker`. 

**Model Training**: 

- The input dataset is split into training, validation, and test datasets using a `data_splitter`. 

- A model is trained! This fits a model using a `hyperparamter_tuner` or just a single `model_trainer`, depending on the configuration. All experiments will be tracked into the `metadata_tracker`. All models created will be versioned and tracked into the `resource_version_control`, also with the data splits themselves. 

- The model is analyzed. This will perform tasks like computing feature importance via a `model_explainer`, running a baseline comparison, and creating visualizations with a `model_visualizer`. 

- Checks are performed on the model with a `model_checker.` This will typically look at things like model error, overfitting, drift, etc. 

- The model is checked for biase using a `model_bias_checker`. This will compute several bias metrics and log them into a `metrics_tracker`. 

- The model lineage is created and tracked in the `metadata_tracker`. 

- A comparison is run between the previous model version and the current model version. This comparison determines if the new model version is better than the previous model version on a static dataset. 

- Optionally, if the new model version is better than the previous ones, the workflow can retrain the model using all available data. This retrains the model given the configuration of the best experiment on the entire dataset. 

**Model Deployment**: 

- Promotes a model using a `model_repository`. 

- Checks if a model has been approved. If so, the model will be deployed using a `model_deployer`. 

**Model Inference**: 

- Compares the incoming prediction data to the training data using a `data_profiler`. Generates a report and saves it to the `metadata_tracker`. 

- Uses the `model_trainer` to generate predictions for the new data. 

- Tracks and versions the new predictions using the `metadata_tracker` and the `resource_version_control`. 

- Compares the current prediction data to the previous prediction data and calculates drift using a `data_profiler`. Generates a report and saves it to the `metadata_tracker`

- Runs checks on the predictions using a `data_checker`. Generates a report and saves it to the `metadata_tracker`. 

- Saves the predictions to a target location via a `data_connector`. 
