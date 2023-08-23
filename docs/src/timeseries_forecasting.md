
This guide will walk us through a quick example of forecasting the sales in a grocery store chain in Ecuador. 

## Setup

1. First, let's create a virtual environment for this example: 

    ```bash
    python3 -m venv ~/venv/grocery_sales
    ```
    Feel free to replace `~/venv/grocery_sales` with any path where you'd like to store the virtual environment. 

    Now, activate the  virtual environment: 

    ```bash
    source ~/venv/grocery_sales/bin/activate
    ```

2. Now let's install the packages we'll need for this example: 

    ```bash 
    pip3 install 'lolop[cli,mlflow,duckdb,timeseries,dvc,optuna]'
    pip3 install tslumen
    ```
    !!! Note 
    The `tslumen` package contains some conflicts with some other dependencies in lolpop that are not utilized in the time series examples. As such, it's not included in an extra, but it's safe to install it for time series workflows.  

3. This example will version data with dvc. In order to use it, we'll need a git repo to use with dvc. For the purposes of this guide, we'll create a git repository in our provider of choice named `lolpop_grocery_sales_example`. You'll then want to clone this repo locally via something like: 

    ```bash 
    git clone git@github.com:<git_user>/lolpop_grocery_sales_example.git
    ```

    Now let's clone the `lolpop` repository to get the files we need for our example. 

    ```bash
    git clone git@github.com:jordanvolz/lolpop.git
    ```

    And then we'll move the grocery_sales example files into our new repository: 

    ```bash
    cp -r lolpop/examples/time_series/grocery_sales/* lolpop_grocery_sales_example
    ```

    Now, we'll move into the `lolpop_grocery_sales_example` directory and set up dvc: 

    ```bash 
    cd lolpop_grocery_sales_example 
    mkdir dvc
    dvc init 
    mkdir /tmp/artifacts
    dvc remote add -d local /tmp/artifacts
    ```

    Note: if you already use dvc, feel free to use a different remote. In this example, we're simply using the local directory `/tmp/artifacts` to store our dvc artifacts. If you use a different remote than local, you'll need to configure that in the `dev.yaml` file to point to the correct remote for the [dvcVersionControl](dvc_resource_version_control.md) class. 

4. Now we'll download the data for the example from Kaggle. If you already use kaggle from the command line you can simply execute the following: 

    ```bash
    kaggle competitions download -c store-sales-time-series-forecasting
    unzip -j -o store-sales-time-series-forecasting.zip train.csv test.csv holidays_events.csv -d data

    ```
    Or, manually download the data from the following [link](https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data) and unzip it. You should now have `train.csv`, `test.csv`, and `holidays_events.csv` files in the `lolpop_grocery_sales_example/data` directory. 

5. In this example we'll also use duckdb as our main data source. To do this, we'll want to ingest our data into duckdb. You can do this via the following command: 

    ```bash 
    python3 setup_duckdb.py
    ```
    This sets up two tables in duckdb that we'll use in this example `total_store_forecast_train` and `total_store_forecast_test`.

## Running the Workflow 

1. To run our workflow, we'll simply need to execute the following command: 

    ```bash 
    python3 run.py 
    ```

2. You should see a bunch of `INFO` messages generated in your terminal. After several minutes your workflow should be finished. The end of your output will look something like: 

    ```bash 
    ...
    2023/08/18 03:50:00.606712 [INFO] <MLFlowMetricsTracker> ::: Saving metric=store_sales_forecast_predictions.num_predictions, value=16 in run 410932cae602426dbe56f4de494f0c68
    2023/08/18 03:50:00.622685 [INFO] <dvcVersionControl> ::: Executing command: `dvc add dvc/store_sales_forecast_predictions.csv`
    100% Adding...|█████████████████████████████████████████████████████████████████████████████████|1/1 [00:00, 17.35file/s]
    2023/08/18 03:50:03.269537 [INFO] <dvcVersionControl> ::: Executing command: `dvc commit dvc/store_sales_forecast_predictions.csv`
    2023/08/18 03:50:06.988464 [INFO] <dvcVersionControl> ::: Committed and pushed file dvc/store_sales_forecast_predictions.csv.dvc. Result: 37c96fb..fb16892

    2023/08/18 03:50:06.989114 [INFO] <dvcVersionControl> ::: Executing command: `dvc push --remote local`
    2023/08/18 03:50:08.824089 [INFO] <dvcVersionControl> ::: Executing command: `dvc get /Users/jordanvolz/github/lolpop_petfinder_example dvc/store_sales_forecast_predictions.csv --show-url`
    2023/08/18 03:50:10.795488 [INFO] <MLFlowMetadataTracker> ::: Saving tag key=store_sales_forecast_predictions.exists, value=True to run 410932cae602426dbe56f4de494f0c68
    2023/08/18 03:50:10.803912 [INFO] <MLFlowMetadataTracker> ::: Saving tag key=store_sales_forecast_predictions.hexsha, value=fb16892da5eee6d9f7940c8150e49ac0730f9f6f to run 410932cae602426dbe56f4de494f0c68
    2023/08/18 03:50:10.806612 [INFO] <MLFlowMetadataTracker> ::: Saving tag key=store_sales_forecast_predictions.uri, value=/tmp/artifacts/5b/1b70482d648e3aa779f559946ed75c
    to run 410932cae602426dbe56f4de494f0c68
    exiting...
    ```

## Exploring the Example 

1. This example uses MLFlow as your metadata tracker, which tracks all the artifacts we're creating. To view them, simply launch MLflow locally: 

    ```bash 
    mlflow ui
    ```

2. You can then open up your web browser and navigate to `http://localhost:5000`. You'll notice an experiment named `store_sales_forecast` with a recently completed run. Feel free to dig around and look at what information got logged. 

3. Predictions from the model get saved to duck db in the `total_store_sales_predictions` table. You can view them via: 

    ```python
    import duckdb

    con = duckdb.connect(database="duckdb/duck.db")

    con.sql("select * from total_store_sales_predictions")
    ```

## Understanding the Example

To get a feel for tracing through the runner, pipeline and component code, see the [quickstart](timeseries_forecasting_quickstart.md) guide. This example follows the same principles, it just does much more. As a summary for what this workflow accomplishes: 

**Data Processing**: 

- Data is transformed via a `data_transformer` component. This would typically involve doing some light data engineering or feature engineering to get data into a single dataset. 

- Data is versioned and tracked using the `metadata_tracker` and the `resource_version_control`

- Data is profiled via a `data_profiler`. This performs an EDA style analysis of the data and save the output report. 

- Data is run through a series of data checks, via a `data_checker`. These checks are typically associated with data quality/integrity. Again, the output report should be saved into the `metadata_tracker`.

**Model Training**: 

- The input dataset is split into training, validation, and test datasets using a `data_splitter`. 

- A model is trained! This fits a model using a `hyperparamter_tuner` or just a single `model_trainer`, depending on the configuration. All experiments will be tracked into the `metadata_tracker`. All models created will be versioned and tracked into the `resource_version_control`, also with the data splits themselves. 

- The model is analyzed. This will perform tasks like running cross validation on the model, running a baseline comparison, and creating visualizations with a `model_visualizer`. 

- The model lineage is created and tracked in the `metadata_tracker`. 

- Optionally, if configured by the user, the workflow can retrain the model using all available data. This retrains the model given the configuration of the best experiment on the entire dataset. 

**Model Deployment**: 

- Promotes a model using a `model_repository`. 

- Checks if a model has been approved. If so, the model will be deployed using a `model_deployer`. 

**Model Inference**: 

- Uses the `model_trainer` to generate predictions for the new data. 

- Tracks and versions the new predictions using the `metadata_tracker` and the `resource_version_control`. 

- Saves the predictions to a target location via a `data_connector`. 
