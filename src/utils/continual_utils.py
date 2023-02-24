### badly needs to be refactored
import os 
import json
from continual import Client 

# Get continual client
def get_client(config): 
    client = Client(
        api_key=config.get("CONTINUAL_APIKEY"), 
        endpoint=config.get("CONTINUAL_ENDPOINT"),
        project=config.get("CONTINUAL_PROJECT"),
        environment=config.get("CONTINUAL_ENVIRONMENT"),
    )
    return client


# Get or return continual run
def get_run(client, description=None, run_id=None): 
    try: 
        run = client.runs.create(description=description, id=run_id)
    except: 
        pass 

    #create doesn't actually error, it just returns None if the resource exists. 
    if run is None: 
        run = client.runs.get(run_id)
    return run 


# Get continual dataset
## Returns dataset,dataset_version as the latter is what you'll likely really want to work with
def get_dataset(run, id, create_dataset_version=False): 
    dataset = run.datasets.create(id)
    dataset_version = None
    if create_dataset_version: 
        dataset_version = dataset.dataset_versions.create()
    return (dataset, dataset_version)

def get_dataset_version(run, id): 
    dataset_version = run.dataset_versions.get(id)


def convert_to_metrics_dicts(metrics): 
    metrics_dicts = []
    value_dicts = []
    for k1 in metrics.keys(): #train/valid/test
        for k2 in metrics[k1].keys(): #metric key
            metrics_dicts.append(
                {
                    "id": k2,
                    "value": metrics[k1][k2],
                    "group": k1,
                }
            )

    return metrics_dicts


#####above here being used#####

def queue_model_for_approval(model_version): 
    return True # not doing approvals right now. handle this later when approvals are supported

def deploy_model(model, config, deployment_framework):
    pass # to do

def get_algo(model_version): 
    exp = get_winning_experiment_from_model_version(model_version)
    algo = exp.metadata.get(key="algorithm").data.replace('"','')
    return algo

#generate local explanations
def get_explanations(model, df, batch_prediction_job, config, explanation_framework, explanation_method, classification_type="multiclass"): 
    if explanation_framework == "continual":
        #need to implement from old code
        pass 

    if explanation_framework == "alibi": 
        if explanation_method == "TreeShap": 
            explainer = TreeShap(model, task="classification")
            explainer.fit()
            explanations = explainer.explain(df)
            get_shap_plots(explanations.shap_values, explanations.expected_value, df, model, "prediction", batch_prediction_job, config, classification_type)

            batch_prediction_job.metadata.create(key="prediction_global_feature_importance", data = explanations.raw.get("importances").get("aggregated"))

            explanations_out = explanations.raw.get("instances").tolist()
    
    return explanations_out 

def log_prediction_metrics(batch_prediction_job, predictions, prediction_col="prediction"): 
    df_values = predictions[prediction_col].value_counts()
    class_distribution = {x:y/sum(df_values) for x,y in df_values.to_dict().items()}

    batch_prediction_job.metadata.create(key="class_distribution", data = class_distribution)
    log_metric("num_predictions", len(predictions), batch_prediction_job)

def save_predictions(predictions, prediction_table, config, type): 
    if type == "snowflake": 
        result = save_to_snowflake(
            predictions, 
            prediction_table,
            config.get("SNOWFLAKE_ACCOUNT"), 
            config.get("SNOWFLAKE_USER"), 
            config.get("SNOWFLAKE_PASSWORD"), 
            config.get("SNOWFLAKE_DATABASE"), 
            config.get("SNOWFLAKE_SCHEMA"), 
            config.get("SNOWFLAKE_WAREHOUSE")
            )
    return result

def save_to_snowflake(predictions, prediction_table, account, user, password, database, schema, warehouse):
    snowflake_credentials = SnowflakeCredentials(
        account=account,
        user=user,
        password=password,
    )
    snowflake_connector = SnowflakeConnector(
        database=database,
        warehouse=warehouse,
        schema=schema,
        credentials=snowflake_credentials
    )
    with snowflake_connector.get_connection() as conn:
        ddl = "PREDICTION INT, PREDICTION_PROBA VARIANT, PETID STRING, EXPLANATION VARIANT"
        statement = f'CREATE TABLE IF NOT EXISTS {prediction_table} ({ddl})'
        with conn.cursor() as cur:
            cur.execute(statement)

        # case sensitivity matters here!
        #df = pd.concat([data["PETID"], pd.DataFrame(predictions, columns=["PREDICTION"])], axis=1)
        success, num_chunks, num_rows, _ = write_pandas(
            conn=conn,
            df=predictions,
            table_name=prediction_table,
            database=snowflake_connector.database,
            schema=snowflake_connector.schema_  # note the "_" suffix
        )

def get_model_version_dataset(model_version): 
    dataset_dict = json.loads(model_version.metadata.get(key="dataset_versions").data)

    # currently we're only working with one dataset. We should rethink this when we have multiple
    # we'd likely want to log the training dataset separately
    training_dataset_version = next(iter(dataset_dict.values()))
    
    return training_dataset_version

def compare_data_to_train(data, model_version, dataset_version, config, run, type): 
    training_dataset_version_name = get_model_version_dataset(model_version)
    training_dataset = run.datasets.get(training_dataset_version_name.split("/")[-3])
    training_dataset_version = training_dataset.dataset_versions.get(training_dataset_version_name)

    train_df = get_dataset_version_dataframe(training_dataset_version, config, type="dvc")
    
    #the following we should refactor w/ compare_data. There is a lot of overlap
    if train_df is None: 
        return 

    if type == "continual": 
        #todo
        pass

    elif type == "sweetviz": 
        data_report = sv.compare([data, "Current Data"], [train_df, "Previous Data"], target_feat = config.get("MODEL_TARGET"))
        data_report.show_html(open_browser=False) 
        file_path =  "%s/SWEETVIZ_REPORT_PREDICTION_TRAIN_DATA_DIFF.html" %os.getcwd()
        artifact = dataset_version.artifacts.create(key = "train_data_comparison", path = file_path, type="html", external=False)

    elif type == "pandas_profiling": 
        profile = ProfileReport(data)
        old_profile = ProfileReport(train_df)
        comparison = profile.compare(old_profile)
        file_path =  "%s/PANDAS_PROFILING_PREDICTION_TRAIN_DATA_DIFF.html" %os.getcwd()
        comparison.to_file(file_path)
        artifact = dataset_version.artifacts.create(key="train_data_comparison", path = file_path, type = "html", external = False)

    elif type == "evidently": 
        data_comparison = TestSuite(tests=[DataStabilityTestPreset(), DataDriftTestPreset()])
        data_comparison.run(reference_data=train_df, current_data=data)
        file_path = "%s/EVIDENTLY_PREDICTION_TRAIN_DATA_DIFF.html" %os.getcwd()
        data_comparison.save_html(file_path)
        artifact = dataset_version.artifacts.create(key = "train_data_comparison", path = file_path, type = "html", external = False)

def get_previous_batch_prediction_job(model_version): 
    previous_batch_prediction_job = None 

    batch_prediction_job_list = model_version.batch_predictions.list(100)
    #objects are not dynamic and we created the model verison before the batch prediction job, 
    # so the last one the mv knows about it actually just the most recent bpj in its history. 
    if len(batch_prediction_job_list) > 0: 
        previous_batch_prediction_job = model_version.batch_predictions.list(100)[-1]

    return previous_batch_prediction_job    

def get_batch_prediction_dataframe(prev_batch_prediction_job, config, type): 
    #these should be basically the same 
    return get_dataset_version_dataframe(prev_batch_prediction_job, config, type)

def calculate_prediction_drift(model_version, batch_prediction_job, predictions, config, type="continual", prediction_col="PREDICTION"): 
    
    prev_batch_prediction_job = get_previous_batch_prediction_job(model_version)
    prev_predictions = get_batch_prediction_dataframe(prev_batch_prediction_job, config, type="dvc")
    
    if prev_predictions is None: 
        return 

    if type == "continual": 
        #todo
        pass

    elif type == "sweetviz": 
        data_report = sv.compare([predictions, "Current Data"], [prev_predictions, "Previous Data"], target_feat = prediction_col)
        data_report.show_html(open_browser=False) 
        file_path =  "%s/SWEETVIZ_PREDICTION_DATA_REPORT.html" %os.getcwd()
        artifact = batch_prediction_job.artifacts.create(key = "prediction_data_comparison", path = file_path, type="html", external=False)

    elif type == "pandas_profiling": 
        profile = ProfileReport(predictions)
        old_profile = ProfileReport(prev_predictions)
        comparison = profile.compare(old_profile)
        file_path =  "%s/PANDAS_PROFILING_PREDICTION_DATA_DIFF.html" %os.getcwd()
        comparison.to_file(file_path)
        artifact = batch_prediction_job.artifacts.create(key="prediction_data_comparison", path = file_path, type = "html", external = False)

    elif type == "evidently": 
        data_comparison = TestSuite(tests=[DataStabilityTestPreset(), DataDriftTestPreset(),  TestColumnDrift(column_name=prediction_col)])
        data_comparison.run(reference_data=prev_predictions[[prediction_col]], current_data=predictions[[prediction_col]])
        file_path = "%s/EVIDENTLY_PREDICTION_DATA_DRIFT.html" %os.getcwd()
        data_comparison.save_html(file_path)
        artifact = batch_prediction_job.artifacts.create(key = "data_comparison", path = file_path, type = "html", external = False)
