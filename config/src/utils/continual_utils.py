### badly needs to be refactored
import pandas as pd
import numpy as np
import os 
import json
import subprocess
import itertools
import optuna
import sweetviz as sv 
import snowflake.connector as snow_conn
from matplotlib import pyplot as plt
import joblib 
import shap 

from pandas_profiling import ProfileReport, compare
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import data_integrity, model_evaluation
from evidently.test_suite import TestSuite
from evidently.test_preset import *
from evidently.tests import * 
from evidently import ColumnMapping
from sklearn import metrics as sk_metrics
from xgboost import XGBClassifier
from alibi.explainers import TreeShap
from yellowbrick.classifier import ClassificationReport, ConfusionMatrix, ROCAUC, PrecisionRecallCurve, DiscriminationThreshold, ClassPredictionError
from yellowbrick.target import ClassBalance, FeatureCorrelation
from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric

from continual import Client 
from continual.python.sdk import utils

from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_snowflake.credentials import SnowflakeCredentials
from prefect_snowflake.database import SnowflakeConnector, snowflake_query
from snowflake.connector.pandas_tools import write_pandas
from git import Repo

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

# get continual model 
## returns model, model_version as the latter is usually what you want to work with 
def get_model(run, id, create_model_version=False): 
    try: 
        model = run.models.create(id)
    except: 
        pass 
    
    if model is None: 
        model = run.models.get(id)
    
    model_version = None
    if create_model_version: 
        model_version = model.model_versions.create() 
    return(model, model_version)

def get_version_method(config): 
    if config.get("DVC_REMOTE", None) is not None: 
        type = "dvc"
    else:
        type = "internal"

    return type

# Version dataframe
## version internally (not recommended)
## or via dvc
def version_data(data, dataset_version, config, type=None):
    artifact_uri = None 
    dataset_id = dataset_version.parent.split("/")[-1]

    if type == None: 
        type = get_version_method(config)

    if type == "internal":
        local_path = "%s/%s__%s.csv" %(os.getcwd(),dataset_id,dataset_version.id)
        data.to_csv(local_path, index=False)
        artifact = dataset_version.artifacts.create(key = "data_csv", path = local_path, type="csv", external=False)
        artifact_uri = artifact.url
    elif type == "dvc": 
        artifact_uri, hexsha = version_data_via_dvc(data, dataset_version, dataset_id, config)
        artifact = dataset_version.artifacts.create(key = "data_csv", url=artifact_uri, type="csv", external=True)
        dataset_version.tags.create(key="git_hexsha", value=hexsha)
    # there's no way to register an externally versioned dataset right now, so the best we can do
    # is just log the URI under metadata
    # if artifact_uri: 
    #    dataset_version.metadata.create(data={"URI": artifact_uri}, type="URI", group_name="data_storage")

    # this probably should be stored as metadata, but right now there's no way to access metadata 
    # without the randomly generated metadata id. Futhermore, we are only having to register this as metadata 
    # because there is not an easy way to recall the artifact used to store the dataframe. 
    dataset_version.tags.create(key="storage_type", value=type)
    dataset_version.tags.create(key="storage_artifact", value=artifact.id)

    return artifact_uri

#version data via dvc. 
def version_data_via_dvc(data, dataset_version, dataset_id, config):
    #assume dvc is already set up. We can handle the case where it is not later
    dvc_path = "%s/%s" %(os.getcwd(),config.get("DVC_DIR"))
    # adding dataset version id to filename track each version separately. 
    # I think we want to let git version via commits instead, but we have to git commit the changes to dvc as well them
    #dvc_file = "%s__%s.csv" %(dataset_id,dataset_version.id)
    dvc_file = "%s.csv" %(dataset_id)
    file_path = "%s/%s" %(dvc_path, dvc_file)
    data.to_csv(file_path, index=False)
    _,_ = execute_cmd("dvc add %s" %file_path)
    _,_ = execute_cmd("dvc commit %s/*" %dvc_path)
    hexsha = git_commit_file("%s.dvc" %file_path)
    _,_ = execute_cmd("dvc push --remote %s" %config.get("DVC_REMOTE"))
    URI,_ = execute_cmd("dvc get %s %s/%s --show-url" %(os.getcwd(), config.get("DVC_DIR"), dvc_file))
    return URI, hexsha

#comits a single file to git
def git_commit_file(file_path, repo_path=None):
    repo = Repo(repo_path)
    repo.index.add(file_path)
    hexsha = repo.index.commit("Commiting dvc file").hexsha

    origin = repo.remotes[0]
    origin.push

    return hexsha


#profiles dataframe based on selected tool. Saves an artifact of the results for non-Continual tooling. 
def profile_data(data, config, run, dataset_version, type="continual"): 
    if type=="continual": 
        #bit of a hack as this function currently requires an index
        df["ID"]=df.index
        dataset_stats_entry = utils.get_dataset_stats_entry_dict(df, "TRAIN", [], "ID", None)
        dataset_version.log_data_profile(stats_entries=[dataset_stats_entry])

    elif type=="sweetviz": 
        data_report = sv.analyze(data, target_feat = config.get("MODEL_TARGET"))
        data_report.show_html(open_browser=False) 
        file_path =  "%s/SWEETVIZ_REPORT.html" %os.getcwd()
        artifact = dataset_version.artifacts.create(key="data_profile", path = file_path, type="html", external=False)

    elif type =="pandas_profiling": 
        profile = ProfileReport(data)
        file_path =  "%s/PANDAS_PROFILING.html" %os.getcwd()
        profile.to_file(file_path)
        artifact = dataset_version.artifacts.create(key = "data_profile", path = file_path, type = "html", external = False)

def get_data_from_dvc(dataset_version, config): 
    dataset_id = dataset_version.parent.split("/")[-1]
    dvc_file = "%s.csv" %(dataset_id)
    hexsha = dataset_version.tags.get("git_hexsha").value
    _,_ = execute_cmd("dvc get %s %s/%s --rev %s -o %s" %(os.getcwd(), config.get("DVC_DIR"), dvc_file, hexsha, dvc_file))
    df = pd.read_csv(dvc_file)
    return df 

#NOTE: we should have a better way to do this in the future
def get_previous_dataset_version(dataset): 
    previous_dataset_version = None 

    dataset_versions_list = dataset.dataset_versions.list(100)
    #if len(dataset_versions_list) > 1: 
    #    previous_dataset_version = dat
    #objects are not dynamic and we craeted the dataset before the dataset version, 
    # so the last one the dataset knows about it actually just the most recent version in its history. 
    if len(dataset_versions_list) > 0: 
        previous_dataset_version = dataset.dataset_versions.list(100)[-1]

    return previous_dataset_version

def get_dataset_version_dataframe(dataset_version, config, type):  
    if type is None: 
        type = dataset_version.tags.get(key="storage_type").value

    if type == "continual": 
       artifact = dataset_version.artifacts.get(key="data_csv")
       os.makedirs(artifact.id, exist_ok=True)
       _, download_path = artifact.download(dest_dir=artifact.id)
       #there should only be one csv, but we return the artifact directory instead of the file itself
       downloaded_csv = [f for f in os.listdir(download_path) if f.endswitch(".csv")]
       df = pd.concat([pd.read_csv(x) for x in downloaded_csv])

    elif type == "dvc": 
       df = get_data_from_dvc(dataset_version, config)

    return df 

#compare data to previous verison
def compare_data(data, config, run, dataset_version, dataset, type="continual"): 
    prev_dataset_version = get_previous_dataset_version(dataset)
    #refersh dv object so we have all up to date info before trying to get df
    dataset_version = dataset.dataset_versions.get(dataset_version.id)
    prev_df = get_dataset_version_dataframe(prev_dataset_version, config, type="dvc")
    
    if prev_df is None: 
        return 

    if type == "continual": 
        #todo
        pass

    elif type == "sweetviz": 
        data_report = sv.compare([data, "Current Data"], [prev_df, "Previous Data"], target_feat = config.get("MODEL_TARGET"))
        data_report.show_html(open_browser=False) 
        file_path =  "%s/SWEETVIZ_REPORT_DIFF.html" %os.getcwd()
        artifact = dataset_version.artifacts.create(key = "data_comparison", path = file_path, type="html", external=False)

    elif type == "pandas_profiling": 
        profile = ProfileReport(data)
        old_profile = ProfileReport(prev_df)
        comparison = profile.compare(old_profile)
        file_path =  "%s/PANDAS_PROFILING_DIFF.html" %os.getcwd()
        comparison.to_file(file_path)
        artifact = dataset_version.artifacts.create(key="data_comparison", path = file_path, type = "html", external = False)

    elif type == "evidently": 
        data_comparison = TestSuite(tests=[DataStabilityTestPreset(), DataDriftTestPreset()])
        data_comparison.run(reference_data=prev_df, current_data=data)
        file_path = "%s/EVIDENTLY_DIFF.html" %os.getcwd()
        data_comparison.save_html(file_path)
        artifact = dataset_version.artifacts.create(key = "data_comparison", path = file_path, type = "html", external = False)

#perform data checks
def data_checks(data, config, run, dataset_version, model_target=None, type="continual"): 
    if type=="continual": 
        #todo -- need to refactor internal data check code 
        pass

    elif type=="deepchecks": 
        ds = Dataset(data, label = model_target, index_name=config.get("MODEL_INDEX"), cat_features=config.get("MODEL_CAT_FEATURES"), datetime_name=config.get("MODEL_TIME_INDEX"))
        data_suite = data_integrity() 
        result = data_suite.run(ds)
        file_path = "%s/DEEPCHECKS_DATA_REPORT.HTML" %os.getcwd()
        result.save_as_html(file_path)
        artifact = dataset_version.artifacts.create(key="data_checks", path = file_path, type = "html", external = False)
        if len(result.get_not_passed_checks()) > 0: 
            raise_alert(msg = "Some deepchecks data checks failed.", type="ERROR")
        elif len(result.get_not_ran_checks()) > 0: 
            raise_alert(msg = "Some deepchecks data checks failed to run.", type="WARNING")

    elif type =="evidently": 
        data_quality = TestSuite(tests=[DataQualityTestPreset()])
        data_quality.run(current_data=data, reference_data=None)
        file_path = "#s/EVIDENTLY_DATA_QUALITY_REPORT.HTML" %os.getcwd()
        data_quality.save_html(file_path)
        artifact = dataset_version.artifacts.create(key="data_checks", path = file_path, type = "html", external = False)
        summary = data_quality.as_dict()["summary"]
        if summary["failed_tests"] > 0: 
            raise_alert(msg = "Some evidently data checks failed.", type="ERROR")
        elif summary["success_tests"] < summary["total_tests"]: 
            raise_alert(msg = "Some evidently data checks failed to run.", type="WARNING")

def raise_alert(msg, type): 
    pass 

def build_split_dfs(train, valid, target,  split_column="SPLIT", test=None): 
    data_out = {
        "X_train" : train.drop([target, split_column], axis=1, errors="ignore"), 
        "X_valid" : valid.drop([target, split_column], axis=1, errors="ignore"), 
        "y_train": train[target], 
        "y_valid": valid[target], 
    }
    #include test set if specified
    if test is not None: 
        data_out["X_test"] = test.drop([target, split_column], axis=1, errors="ignore")
        data_out["y_test"] = test[target]

    return data_out

#function to split data. Supports random splitting, manual splitting, and stratified. Can also include test set. 
def split_data(data, target,  split_column=None, split_classes={},  split_ratio=[0.8,0.2], sample_num=100000, use_startified=False, include_test=False): 
    data_out = {}
    test = None 

    #if a split_column is provided, then we assume you wanted to handle everything yourself
    if split_column is not None: 
        train = data[data[split_column] == split_classes["train"]]
        valid = data[data[split_column] == split_classes["valid"]]
        if include_test: 
            test = data[data[split_column] == split_classes["test"]]
        data_out = build_split_dfs(train, valid, target, split_column, test)

    else: #random sample
        if use_startified: 
            strat_df = data.groupby(target, group_keys=False).apply(lambda x: x.sample(min(len(x), 2)))
        if data.shape[0] > sample_num: 
            data = data.sample(sample_num)

        train = data.sample(frac=split_ratio[0])
        valid = data.drop(train.index)
        
        if include_test: 
            temp_valid = valid.copy()
            valid = temp_valid.sample(frac=split_ratio[1])
            test = temp_valid.drop(valid.index)
        
        if use_startified: 
            train = train.merge(strat_df, how="outer")
            valid = valid.merge(strat_df, how="outer")
            if include_test:
                test = test.merge(strat_df, how="outer")
         
        data_out = build_split_dfs(train, valid, target, test=test)

    return data_out 
        
# starting with something simple: xgboost
# If youw want to implment a different framework w/ hyperparam tuning, check out
# optuna examples: https://github.com/optuna/optuna-examples

def build_training_grid(params): 
    keys, values = zip(*params.items())
    values = [v if isinstance(v, list) else v.split(",") for v in values]
    grid = [dict(zip(keys,v)) for v in itertools.product(*values)]

    return grid

#version model via dvc. 
def version_model_via_dvc(model, model_version, algo, experiment, config):
    #assume dvc is already set up. We can handle the case where it is not later
    dvc_path = "%s/%s" %(os.getcwd(),config.get("DVC_DIR"))
    model_file = "model/%s/%s/%s" %(model_version.id, algo, experiment.id)  
    model_path = "%s/%s" %(dvc_path, model_file)  
    joblib.dump(model, model_path)
    _,_ = execute_cmd("dvc add %s" %model_path)
    _,_ = execute_cmd("dvc commit %s/*" %dvc_path)
    hexsha = git_commit_file("%s.dvc" %model_path)
    _,_ = execute_cmd("dvc push --remote %s" %config.get("DVC_REMOTE"))
    URI,_ = execute_cmd("dvc get %s %s --show-url" %(os.getcwd(), config.get("DVC_DIR"), model_file))
    return URI, hexsha

def save_model(model, config, algo, model_version, experiment, type=None): 

    if type == None: 
        type = get_version_method(config)

    if type == "continual":
        model_dir = "%s/model/%s/%s" %(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), model_version.id, algo)    
        os.makedirs(model_dir, exist_ok=True)
        model_path = "%s/%s" %(model_dir, experiment.id)
        joblib.dump(model, model_path)
        artifact = experiment.artifacts.create(key = "model_artifact", path=model_path, external=False, upload=True)
    elif type == "dvc": 
        artifact_uri, hexsha = version_model_via_dvc(model, model_version, algo, experiment, config)
        artifact = experiment.artifacts.create(key = "model_artifact", url=artifact_uri, type="csv", external=True)
        experiment.tags.create(key="git_hexsha", value=hexsha)

    experiment.tags.create(key="storage_type", value=type)
    experiment.tags.create(key="storage_artifact", value=artifact.id)

    return artifact 

def build_model(data, config, algo, params, model_version, version_type): 
    #create experiment and log params
    experiment = model_version.experiments.create() 
    experiment.metadata.create(key="training_params", data=params)
    experiment.metadata.create(key="algorithm", data=algo)

    if algo == "xgboost": 
        clf = XGBClassifier(**params)
        clf.fit(data["X_train"], data["y_train"])
    else: #only xgboost implemented right now
        pass 

    save_model(clf, config, algo, model_version, experiment, version_type)
    #consider saving train/vali/test here too. We are already versioning the dataset, but it may be nice
    #to explicitly version the splits as well to remove ambiguitity if you're using random splits, etc. 

    return clf, experiment

def get_predictions_from_df(model, df, df_index, algo): 
    predictions = pd.DataFrame()

    if algo == "xgboost": 
        predictions["PREDICTION"] = model.predict(df)
        predictions["PREDICTION_PROBA"] = model.predict_proba(df).tolist()

    #model often does not include the index as a feature, so set it here
    predictions[df_index.name] = df_index

    return predictions 

def get_predictions(model, data, algo): 
    predictions = {}

    if algo == "xgboost": 
        predictions["train"] = model.predict(data["X_train"])
        predictions["valid"] = model.predict(data["X_valid"])
        predictions["train_proba"] = model.predict_proba(data["X_train"])
        predictions["valid_proba"] = model.predict_proba(data["X_valid"])

        if data.get("X_test") is not None: 
            predictions["test"] = model.predict(data["X_test"])
            predictions["test_proba"] = model.predict_proba(data["X_test"])
    return predictions

def calculate_metrics(data, predictions, metrics, problem_type="classification"): 
    metrics_out = {"train" : {}, "valid" : {}, "test" : {}}

    test_exists = data.get("X_test") is not None

    if problem_type == "classification": 
        multi_class = False
        average="binary"
        num_classes = len(data["y_train"].unique())
        if num_classes > 2: 
            multi_class = True 
            average = "weighted"

    for metric in metrics: 
        if metric == "accuracy": 
            metrics_out["train"][metric] = sk_metrics.accuracy_score(data["y_train"], predictions["train"])
            metrics_out["valid"][metric] = sk_metrics.accuracy_score(data["y_valid"], predictions["valid"])
            if test_exists:
                metrics_out["test"][metric] = sk_metrics.accuracy_score(data["y_test"], predictions["test"])
        if metric == "f1": 
            metrics_out["train"][metric] = sk_metrics.f1_score(data["y_train"], predictions["train"], average = average)
            metrics_out["valid"][metric] = sk_metrics.f1_score(data["y_valid"], predictions["valid"], average = average)
            if test_exists:
                metrics_out["test"][metric] = sk_metrics.f1_score(data["y_test"], predictions["test"], average = average)
        if metric == "rocauc": 
            metrics_out["train"][metric] = sk_metrics.roc_auc_score(data["y_train"], predictions["train_proba"], average = average, multi_class = "ovr")
            metrics_out["valid"][metric] = sk_metrics.roc_auc_score(data["y_valid"], predictions["valid_proba"], average = average, multi_class = "ovr")
            if test_exists:
                metrics_out["test"][metric] = sk_metrics.roc_auc_score(data["y_test"], predictions["test_proba"], average = average, multi_class = "ovr")
        if metric == "prauc": 
            if not multi_class: 
                metrics_out["train"][metric] = sk_metrics.average_precision_score(data["y_train"], predictions["train_proba"][:,1])
                metrics_out["valid"][metric] = sk_metrics.average_precision_score(data["y_valid"], predictions["valid_proba"][:,1])
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.average_precision_score(data["y_test"], predictions["test_proba"][:,1])
        if metric == "precision": 
            metrics_out["train"][metric] = sk_metrics.precision_score(data["y_train"], predictions["train"], average = average)
            metrics_out["valid"][metric] = sk_metrics.precision_score(data["y_valid"], predictions["valid"], average = average)
            if test_exists:
                metrics_out["test"][metric] = sk_metrics.precision_score(data["y_test"], predictions["test"], average = average)
        if metric == "recall": 
            metrics_out["train"][metric] = sk_metrics.recall_score(data["y_train"], predictions["train"], average = average)
            metrics_out["valid"][metric] = sk_metrics.recall_score(data["y_valid"], predictions["valid"], average = average)
            if test_exists:
                metrics_out["test"][metric] = sk_metrics.recall_score(data["y_test"], predictions["test"], average = average)

    return metrics_out




def log_metrics(exp, metrics, perf_metric): 
    # Need to use proper update mechanism once available. This doesn't actually get saved 
    exp.performance_metric_name = perf_metric
    exp.performance_metric_value = metrics["valid"][perf_metric]

    metrics_dicts = convert_to_metrics_dicts(metrics)
    
    for metric in metrics_dicts: 
        exp.metrics.create(**metric)
    
def get_metric_direction(perf_metric): 
    reverse = False 
    if perf_metric in ["mse", "rmse", "mae", "mape", "smape"]: 
        reverse = True 
    return reverse

def get_winning_experiment(exp_list, perf_metric): 
    reverse = get_metric_direction(perf_metric)
    new_list = sorted(exp_list.items(), key=lambda x: x[1], reverse=reverse) # sort list by values
    return new_list[0][0]

#this is necessary because we need to refesh objects as they are not dynamic
def get_experiment(model_version, winning_exp_id, run): 
    model = run.models.get(model_version.parent)
    mv = model.model_versions.get(model_version.id)
    exp = mv.experiments.get(winning_exp_id)

    return exp 


def get_model_from_dvc(experiment, config): 
    model_version_id = experiment.parent.split("/")[-1]
    algo = experiment.metadata.get("algrithm").data
    dvc_file = "model/%s/%s/%s" %(model_version_id,algo,experiment.id)
    hexsha = experiment.tags.get("dvc_hexsha").value
    _,_ = execute_cmd("dvc get %s %s/%s --rev %s -o %s" %(os.getcwd(), config.get("DVC_DIR"), dvc_file, hexsha, dvc_file))
    model = joblib.load(dvc_file)
    return model

def get_experiment_model(exp, config, type):
    if type is None: 
        type = dataset_version.tags.get(key="storage_type").value

    if type == "continual": 
        artifact = exp.artifacts.get(key="model_artifact")
        os.makedirs(artifact.id, exist_ok=True)
        _, download_path = artifact.download(dest_dir=artifact.id)
        #there should only be one csv, but we return the artifact directory instead of the file itself
        model = joblib.load(download_path)
    elif type == "dvc":
        model = get_model_from_dvc(model, config)
    
    return model

#        {
    #         "objective": {"type": "categorical", "choices" : ["multiclass"]},
    #         "max_depth": {"type": "int", "range" : [4,8]},
    #         "alpha": {"type": "float", "range" : [1,10]},
    #         "learning_rate": {"type": "float", "range" : [0.1,1]},
    #         "n_estimators": {"type": "int", "range" : [1,10]},
    #         "random_state": {"type": "fixed", "value" : 0},
    #     }

# parses each value of a dynamic config to the optuna type
def parse_dynamic_logic(trial, name, p):
    type = p.get("type")

    if type == "fixed": 
        return p.get("value")
    elif type == "int": 
        low_high = p.get("range")
        return trial.suggest_int(name, low_high[0], low_high[1])
    elif type == "float":
        low_high = p.get("range")
        return trial.suggest_float(name, low_high[0], low_high[1])
    elif type == "categorical":
        choices = p.get("choices")
        return trial.suggest_categorical(name, choices)

def get_dynamic_params(trial, params):
    params_out = {}
    for p in params: 
        params_out[p] = parse_dynamic_logic(trial, p, params[p])
    return params_out

def get_fixed_params(trial, params): 
    params_out = {}
    for p in params: #since the params passed for a fixed set are static, we can represent them as a categorical
        params_out[p] = trial.suggest_categorical(p, params[p])
    return params_out

def log_trial(trial, params, model, model_version, config, algo, version_type):
    experiment = model_version.experiments.create() 
    experiment.metadata.create(key="training_params", data=params)
    experiment.metadata.create(key="algorithm", data=algo)
    #we should log start/stop time here when it's updateable in the sdk

    save_model(model, config, algo, model_version, experiment, version_type)

    return experiment

# objective function used for optuna. Optimizes over the provided per_metric. 
# supports fixed and dynamic parameters
def optuna_xgboost_objective(trial, type, data, model_version, config, params, metrics, perf_metric, version_type): 
    #if we are dynamic we just need to modify the paramst to use suggest_x to dynamically create values 

    if type == "dynamic": 
        model_params = get_dynamic_params(trial, params)
    else: #type=="fixed"
        model_params = get_fixed_params(trial, params)
    clf = XGBClassifier(**model_params)
    clf.fit(data["X_train"], data["y_train"])
    predictions = get_predictions(clf, data, "xgboost")
    metrics = calculate_metrics(data, predictions, metrics) #only need to calculate perf metric for selection
    perf_metric_value = metrics["valid"][perf_metric]

    # save_model
    # need to save model now because optuna doesn't provide access to models later on. 
    #use model_params instaed of trial.params as optuna doesn't track fixed parameters, but the user may want to
    experiment = log_trial(trial, model_params, clf, model_version, config, "xgboost", version_type)
    log_metrics(experiment, metrics, perf_metric)

    #save experiment id in trial attributes so we can refer back to it later 
    trial.set_user_attr("experiment_id", experiment.id)

    return perf_metric_value

def run_optuna_study(trial, type, data, continual_run, training_params, config, model_version, version_type, metrics, perf_metric): 

    if algo =="xgboost": 
        study = optuna_xgboost_objective()

#saves plot (internally)
def save_plot(name, plot, model_version, algo): 
    local_path = "%s/%s/%s" %(os.getcwd(), model_version.id, algo)
    os.makedirs(local_path, exist_ok=True)
    local_file = "%s/%s" %(local_path, name)
    plot.write_html(local_file)
    artifact = model_version.artifacts.create(key = name, path = local_file, type="html", external=False, upload = True)

#saves interesting parts of the study
def log_study(study, model_version, algo): 
    # iterate through each trial and log appropriate pieces into continual
    if optuna.visualization.is_available(): 
        plot = optuna.visualization.plot_edf(study)
        save_plot("plot_edf.html",plot, model_version,algo)

        #only useful if using intermediate values and pruning
        #plot = optuna.visualization.plot_intermediate_values(study)
        #save_plot("plot_intermediate_values.html",plot, model_version,algo)

        plot = optuna.visualization.plot_optimization_history(study)
        save_plot("plot_optimization_history.html",plot, model_version,algo)

        plot = optuna.visualization.plot_parallel_coordinate(study)
        save_plot("plot_parallel_coordinate.html",plot, model_version,algo)

        plot = optuna.visualization.plot_param_importances(study)
        save_plot("plot_param_importances.html",plot, model_version,algo)

        #only used for multi-objective studies
        #optuna.visualization.plot_pareto_front(study)
        #save_plot("plot_pareto_front.html",plot, model_version,algo)

        plot = optuna.visualization.plot_slice(study)
        save_plot("plot_slice.html",plot, model_version,algo)

        plot = optuna.visualization.plot_contour(study)
        save_plot("plot_contour.html",plot, model_version,algo)


# run a single experiment set for a model version 
# this got pretty long, so it should probably be refactored 
def run_experiment(data, continual_run, training_params, config, model_version, metrics, perf_metric, hyperopt_tool="continual", version_type="continual", n_trials=100, timeout=600): 

    # params can call different algos and user hyperparam tuning, etc 
    # first we generated a list of experiments + scores    
    if hyperopt_tool == "continual": 
        exp_list = {}
        for algo in training_params: 
            grid = build_training_grid(training_params[algo])
            for params in grid: 
                clf, exp = build_model(data, config, algo, params, model_version, version_type)
                predictions = get_predictions(clf, data, algo)
                metrics_val = calculate_metrics(data, predictions, metrics)
                log_metrics(exp, metrics_val, perf_metric)
                exp_list[exp.id] = metrics_val["valid"][perf_metric]

    elif hyperopt_tool == "optuna":
        try:  
            type = training_params.pop("type")
        except: 
            type = "fixed"

        #understand if we want to minimize or maximum objective for optuna
        reverse = get_metric_direction(perf_metric)
        if reverse: 
            direction = "minimize"
        else: 
            direction = "maximize"

        exp_list = {} 
        for algo in training_params: 
            #need to create study w/ sampler so that the results are reproducible later on
            sampler = optuna.samplers.TPESampler(seed=42) 
            study = optuna.create_study(direction=direction, sampler=sampler)
            if type == "fixed":
                grid = build_training_grid(training_params[algo])
                #enqueue all fixed params
                for params in grid: 
                    study.enqueue_trial(params)   
                #only run n_trials = len(grid) to only run enqued params
                n_trials = len(grid)
            #    study.optimize(lambda trial: optuna_xgboost_objective(trial, type, data, model_version, config, params, metrics, perf_metric, version_type), n_trials=len(grid), timeout=timeout)
            #else: #type == "dynamic"
            study.optimize(lambda trial: optuna_xgboost_objective(trial, type, data, model_version, config, training_params[algo], metrics, perf_metric, version_type), n_trials=n_trials, timeout=timeout)
            #log study
            study.set_user_attr("perf_metric", perf_metric)
            study.set_user_attr("perf_metric_val", study.best_value)
            log_study(study, model_version, algo) #returns best exp id 
            best_experiment = study.best_trial.user_attrs.get("experiment_id")
            exp_list[best_experiment] = "value"

    #now, we determine overall best experiment and save into model_version
    winning_exp_id = get_winning_experiment(exp_list, perf_metric)
    winning_exp = get_experiment(model_version, winning_exp_id, continual_run)
    best_clf = get_experiment_model(winning_exp, config, version_type) 
    for metric in winning_exp.metrics.list():
        model_version.metrics.create(**metric)
    #none of these below are updateable right now, revisit once the pr gets in. 
    #model_version.performance_metric_name = winning_exp.performance_metric_name
    #model_version.performance_metric_value = winning_exp.performance_metric_val
    #model_version.experiment_name = winning_exp.name
    model_version.metadata.create(key="winning_experiment_name", data=winning_exp.name)
    
    return best_clf

def get_train_test_dfs(data, combine_xy=True, combine_train_valid=True):
    if combine_train_valid: 
        df_X = pd.concat([data["X_train"],data["X_valid"]])
        df_y = pd.concat([data["y_train"],data["y_valid"]])
    else: 
        df_X = data["X_train"]
        df_y = data["y_train"]

    if combine_xy: 
        train = pd.concat([df_X,df_y],axis=1)
        test = pd.concat([data["X_test"], data["y_test"]], axis=1)
    else: 
        train = (df_X, df_y)
        test = (data["X_test"], data["y_test"])

    return train, test 

#labels should be something like data["y_train"].unique()
def get_multiclass(labels): 
    classification_type = "binary"
    num_classes = len(labels)
    if num_classes > 2: 
        classification_type = "multiclass"

    return classification_type

#perform model checks
def model_checks(model, data, config, run, model_version, type="continual"): 
    df_train, df_test = get_train_test_dfs(data) 

    classification_type = get_multiclass(data["y_train"].unique())

    if type=="continual": 
        #todo -- need to refactor internal model check code 
        pass

    elif type=="deepchecks": 
        ds_train = Dataset(df_train, label = config.get("MODEL_TARGET"), index_name=config.get("MODEL_INDEX"), cat_features=config.get("MODEL_CAT_FEATURES"), datetime_name=config.get("MODEL_TIME_INDEX"))
        ds_test = Dataset(df_test, label = config.get("MODEL_TARGET"), index_name=config.get("MODEL_INDEX"), cat_features=config.get("MODEL_CAT_FEATURES"), datetime_name=config.get("MODEL_TIME_INDEX"))
      
        model_suite = model_evaluation() 
        result = model_suite.run(ds_train, ds_test, model)

        file_path = "%s/DEEPCHECKS_MODEL_REPORT.HTML" %os.getcwd()
        result.save_as_html(file_path)
        artifact = model_version.artifacts.create(key="model_checks", path = file_path, type = "html", external = False)
        
        if len(result.get_not_passed_checks()) > 0: 
            raise_alert(msg = "Some deepchecks model checks failed.", type="ERROR")
        elif len(result.get_not_ran_checks()) > 0: 
            raise_alert(msg = "Some deepchecks model checks failed to run.", type="WARNING")

    elif type =="evidently": 
        column_mapping = ColumnMapping()
        column_mapping.target=config.get("MODEL_TARGET")
        column_mapping.prediction="prediction"
        df_train["prediction"] = model.predict(df_train.drop([config.get("MODEL_TARGET")], axis=1))
        df_test["prediction"] = model.predict(df_test.drop([config.get("MODEL_TARGET")], axis=1))

        if classification_type == "multiclass": 
            classification_test = TestSuite(tests=[MulticlassClassificationTestPreset(), NoTargetPerformanceTestPreset(), TestColumnDrift(column_name=config.get("MODEL_TARGET"))])
        else: 
            classification_test = TestSuite(tests=[BinaryClassificationTestPreset(), NoTargetPerformanceTestPreset(), TestColumnDrift(column_name=config.get("MODEL_TARGET"))])
        classification_test.run(current_data=df_test, reference_data=df_train, column_mapping=column_mapping)
        file_path = "%s/EVIDENTLY_CLASSIFICATION_MODEL_REPORT.HTML" %os.getcwd()
        classification_test.save_html(file_path)
        artifact = model_version.artifacts.create(key="model_checks", path = file_path, type = "html", external = False)
        summary = classification_test.as_dict()["summary"]
        if summary["failed_tests"] > 0: 
            raise_alert(msg = "Some evidently model checks failed.", type="ERROR")
        elif summary["success_tests"] < summary["total_tests"]: 
            raise_alert(msg = "Some evidently model checks failed to run.", type="WARNING")

#save plot from matplotlib
def save_pyplot(name, label, model_version): 
    local_path = "%s/%s/%s" %(os.getcwd(), model_version.id, label)
    os.makedirs(local_path, exist_ok=True)
    key = "%s_%s"%(name, label)
    local_file = "%s/%s.png" %(local_path, key)
    plt.savefig(local_file)
    artifact = model_version.artifacts.create(key = key, path = local_file, type="png", external=False, upload = True)
    #plt.clf()
    plt.close()

#generate all the shap plot
def get_shap_plots(shap_values, expected_value, data, model, label, model_version, config, classification_type): 
    
    if classification_type == "multiclass":
        #bar plot w/ all classes
        shap.summary_plot(shap_values, data)
        save_pyplot("shap_summary_plot_bar", label, model_version)
    else: 
        #if binary, then just make it an array of one class and the rest should still work
        shap_values = [shap_values]

    #for multiclass, many plots only work on one class at a time. 
    for i in range(len(shap_values)):
        #scatter plot for class
        shap.summary_plot(shap_values[i], data)
        save_pyplot("shap_scatter_plot_class_%s" %str(i), label, model_version)
        #bar plot for class
        shap.summary_plot(shap_values[i], data, plot_type="bar")
        save_pyplot("shap_scatter_plot_bar_%s" %str(i), label, model_version)
        ##force plot for class
        ##force plot is very slow for large matrices, so we'll impose a sample
        sample_size = 100
        idx = np.random.randint(len(shap_values[i]), size=sample_size)
        # force plot doesn't really work w/ multiclass right now
        #shap.force_plot(expected_value[i], shap_values[i][idx,:], matplotlib=True)
        #save_pyplot("shap_force_plot_bar_%s" %str(i), label, model_version)
        shap.decision_plot(expected_value[i], shap_values[i][idx,:])
        save_pyplot("shap_decision_plot_%s" %str(i), label, model_version)
        #create dependence plots -- one for each feature
        for ft in data.columns: 
            #you can set interaction_index to determine which feature is used to color plot.
            #if omitted it will just use what seems to have the best interaction. If none it will turn off coloring
            shap.dependence_plot(ft, shap_values[i], data, interaction_index=None)
            save_pyplot("shap_dependence_plot_%s_%s" %(str(i), ft), label, model_version)
            #partial dependence
            if i == 0: #only need to calculate these once
                shap.partial_dependence_plot(ft, model.predict, data)
                save_pyplot("shap_partial_dependence_plot_%s" %ft, label, model_version)
        # we can also check bias too: 
        #for bias in config.get('BIAS_COLUMNS').split(","): 
        #    shap.group_difference_plot(shap_values[i], data[bias].values==1, feature_names=data.columns)
        #    save_pyplot("shap_group_difference_plot_%s_bias_%s" %(str(i),bias), label, model_version)
        

        #other plots
        #waterfall_plot only shows the effect of one row at a time
        #multioutput_decision_plot only shows the effect of one row at a time, but it's super awesome for multiclass problems
        #heatmap -- difficult to use from alibi

def compare_train_test_feat_importance(explanations_train, explanations_test, classification_type, threshold=0.25): 
    shap_train = explanations_train.shap_values
    shap_test = explanations_test.shap_values

    #make everything 3dim so the following code is the same regardless of type
    if classification_type !="multiclass": 
        shap_train= [shap_train]
        shap_test = [shap_test]


    #check expected values 
    if classification_type == "multiclass": 
        expected_diff = [(x - y)/max(x, 0.00001) for x,y in zip(explanations_train.expected_value, explanations_test.expected_value)]
    else: 
        expected_diff = [shap_train.expected_value - shap_test.expected_value]

    for x in expected_diff: 
        if x> threshold: 
            raise_alert(msg = "Threshold exceeded in difference between train/test shap expected values.", error="WARNING")

    #check avg value for feature
    # we could recalculate everything, but shap provides the globals in the aggregated features
    #np_train = np.array(shap_train)
    #train_ft_values = np.abs(np_train).mean(axis=0).mean(axis=0)
    #np_test = np.array(shap_test)
    #test_ft_values = np.abs(np_test).mean(axis=0).mean(axis=0)

    raw_train_importances = explanations_train.raw.get("importances").get("aggregated")
    raw_test_importances = explanations_test.raw.get("importances").get("aggregated")
    # sort values to ensure features match up
    train_ft_values = sorted(
        [ x[1] for x in  zip(raw_train_importances.get("names"), raw_train_importances.get("ranked_effect"))] 
        ) 
    test_ft_values = sorted(
        [ x[1] for x in  zip(raw_test_importances.get("names"), raw_test_importances.get("ranked_effect"))]
        ) 

    feature_diff = [(x-y)/max(x, 0.00001) for x,y in zip(train_ft_values, test_ft_values)]

    for x in feature_diff: 
        if x > threshold: 
            raise_alert(msg = "Threshold exceeded in difference between a feature shap value impact in train & test datasets.", error="WARNING")

    return expected_diff, feature_diff

def log_global_feature_importance(explanations_train, explanations_test, expected_value_diff, feature_importance_diff, model_version): 
    
    model_version.metadata.create(key="train_global_feature_importance", data = explanations_train.raw.get("importances").get("aggregated"))
    model_version.metadata.create(key="test_global_feature_importance", data = explanations_test.raw.get("importances").get("aggregated"))
    model_version.metadata.create(key = "feature_importance_expected_value_diff_train_test", data = expected_value_diff)
    model_version.metadata.create(key = "feature_importance_feature_value_diff_train_test", data = feature_importance_diff)

#generate feature importance
def get_feature_importance(model, data, model_version, config, explanation_framework, explanation_method): 
    (train_X, train_y), (test_X, test_y) = get_train_test_dfs(data, combine_xy=False) 

    classification_type = get_multiclass(train_y.unique())

    if explanation_framework == "continual":
        #need to implement from old code
        pass 

    if explanation_framework == "alibi": 
        if explanation_method == "TreeShap": 
            explainer = TreeShap(model, task="classification")
            explainer.fit()
            explanations_train = explainer.explain(train_X)
            explanations_test = explainer.explain(test_X)
            get_shap_plots(explanations_train.shap_values, explanations_train.expected_value, train_X, model, "train", model_version, config, classification_type)
            get_shap_plots(explanations_test.shap_values, explanations_test.expected_value, test_X, model, "test", model_version, config, classification_type)

            #compare test and train? 
            expected_value_diff, feature_importance_diff = compare_train_test_feat_importance(explanations_train, explanations_test, classification_type)
            
            log_global_feature_importance(explanations_train, explanations_test, expected_value_diff, feature_importance_diff, model_version)

    return explanations_train, explanations_test

def get_metric_comparison(champion_metric, challenge_metric, perf_metric): 
    old_metric = champion_metric.get("test").get(perf_metric)
    new_metric = challenge_metric.get("test").get(perf_metric)
    metric_direction = get_metric_direction(perf_metric)

    if metric_direction: #True = perf_metric is better if lower
        is_baseline_better = (new_metric <= old_metric) 
    else: #wants higher perf metric
        is_baseline_better = (new_metric >= old_metric )

    metric_diff = (old_metric - new_metric) / max(old_metric,0.00001) 

    return is_baseline_better, metric_diff

def get_baseline_predictions(data, BASELINE_METHOD, BASELINE_VALUE): 
    #column = user defined column should be used for baseline comparison
    has_test = "X_test" in data.keys()
    baseline_predictions = {}

    if BASELINE_METHOD == "COLUMN": 
        baseline_predictions["train"] = data["X_train"][BASELINE_VALUE]
        baseline_predictions["valid"] = data["X_valid"][BASELINE_VALUE]
        if has_test: 
            baseline_predictions["test"] = data["X_test"][BASELINE_VALUE]

    elif BASELINE_METHOD == "VALUE":    
        labels = data["y_train"]
        #this is kind of hacky but ... shrug
        labels.index=labels.values
        label_counts = labels.groupby(level=0).count()

        if BASELINE_VALUE == "class_avg": 
            weights = [x/len(labels) for x in label_counts]
            baseline_predictions["train"] = np.random.choice(label_counts.index, p=weights, size=len(data["X_train"]))
            baseline_predictions["valid"] = np.random.choice(label_counts.index, p=weights, size=len(data["X_valid"]))
            if has_test: 
                baseline_predictions["test"] = np.random.choice(label_counts.index, p=weights, size=len(data["X_test"]))

        elif BASELINE_VALUE == "class_most_frequent": 
            most_frequent_class = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)[0][0] #get most frequent class 
            baseline_predictions["train"] = [most_frequent_class] * len(data["X_train"])
            baseline_predictions["valid"] = [most_frequent_class] * len(data["X_valid"])
            if has_test: 
                baseline_predictions["test"] = [most_frequent_class] * len(data["X_test"])

    else: #consider other ways to do baseline comparison
        pass

    return baseline_predictions 

def get_baseline_comparision(model, data, model_version, config, BASELINE_METHOD, BASELINE_VALUE, perf_metric):

    #TODO: we are already getting predictions elsewhere. We should just save them and pass in instead of calculating again
    exp = get_winning_experiment_from_model_version(model_version)
    algo = exp.metadata.get(key="algorithm").data.replace('"','')
    test_predictions = get_predictions(model, data, algo)
    baseline_predictions = get_baseline_predictions(data, BASELINE_METHOD, BASELINE_VALUE)

    #again, model metrics are being recalculated here, should save and load
    model_metrics = calculate_metrics(data, test_predictions, [perf_metric], problem_type="classification")
    baseline_metrics = calculate_metrics(data, baseline_predictions, [perf_metric], problem_type="classification")
    is_baseline_better, metric_diff = get_metric_comparison(model_metrics, baseline_metrics, perf_metric)

    log_metric("model_test_performance_over_baseline", metric_diff, model_version)

    if is_baseline_better: 
        raise_alert(msg = "Model performed worse than baseline by %s%" %metric_diff, error="WARNING")

    return metric_diff 

def save_yb_plots(viz, data, model_version, plot_name): 
    splits =["train", "valid", "test"]
    viz.fit(data["X_train"], data["y_train"])

    for split in splits: 
        viz.score(data["X_%s" %split], data["y_%s" %split])
        save_pyplot(plot_name, split, model_version)

def get_model_viz(model, data, model_version, config, VIZ_TOOL, classification_type="multiclass"): 
    
    classification_type = get_multiclass(data["y_train"])

    #metric report
    viz = ClassificationReport(model)
    save_yb_plots(viz, data, model_version, "yb_classification_report")

    #confusion matrix
    viz = ConfusionMatrix(model)
    save_yb_plots(viz, data, model_version, "yb_confusion_matrix")

    #rocauc
    viz = ROCAUC(model)
    save_yb_plots(viz, data, model_version, "yb_rocauc")

    #comment out for now -- errors if not all classes are represented in the predictions
    ##pr curve
    #viz = PrecisionRecallCurve(model, per_class=True) #per class handles multiclass use cases
    #save_yb_plots(viz, data, model_version, "yb_prauc")

    #class error
    viz = ClassPredictionError(model)
    save_yb_plots(viz, data, model_version, "yp_class_error")

    if classification_type == "binary":
        #discrimination threshold -- only works for binary
        viz = DiscriminationThreshold(model) 
        save_yb_plots(viz, data, model_version, "yb_disctreshold")

    #class balance
    viz = ClassBalance()
    viz.fit(data["y_train"])
    save_pyplot("yb_class_balance", "train", model_version)

    #class balance
    viz = FeatureCorrelation(labels=data["X_train"].columns)
    viz.fit(data["X_train"],data["y_train"])
    save_pyplot("yb_feature_correlation", "train", model_version)

    #note: could be fun to add some model selection viz here as well: https://www.scikit-yb.org/en/latest/api/model_selection/index.html
    # and yb has some interesting feature analysis viz that we could use in data processing: https://www.scikit-yb.org/en/latest/api/features/index.html

def log_metric(name, value, model_version, direction="UP"): 
    metric = {
            "key": name,
            "value": value,
            "direction": direction,
        }

    model_version.metrics.create(**metric)

def get_model_bias(model, data, model_version, config, BIAS_PARAMS): 

    df_train = data["X_train"]
    df_train_w_labels = df_train.copy() 
    df_train_w_labels["ADOPTIONSPEED"] = data["y_train"].values
    preds = model.predict(df_train)

    #parse bias_params and handle each framework separately
    for framework in BIAS_PARAMS.keys(): 
        if framework == "AIF360" : #only aif360 supported right now 
            ds = StandardDataset(
                df=df_train_w_labels.dropna(), #NA make AI360 fail 
                label_name=config.get("MODEL_TARGET"), 
                protected_attribute_names=BIAS_PARAMS.get(framework).get("protected_attribute_names"), 
                favorable_classes=BIAS_PARAMS.get(framework).get("favorable_classes"), 
                privileged_classes=BIAS_PARAMS.get(framework).get("privileged_classes"),
                )

            privileged_groups = BIAS_PARAMS.get(framework).get("privileged_groups")
            unprivileged_groups = BIAS_PARAMS.get(framework).get("unprivileged_groups")

            #get fairness metrics from binarylabeldatasetmetric. This essentially checks bias in the dataset itself
            bldm = BinaryLabelDatasetMetric(ds, unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
            log_metric("bldm_base_rate", bldm.base_rate(), model_version) # ratio of priv/total 
            log_metric("bldm_disparate_impact", bldm.disparate_impact(), model_version) # ratio of prob fav outcomes of non/priv
            log_metric("bldm_mean_difference",  bldm.mean_difference(), model_version) # diff in probability of favorable outcoems for non vs priv
            log_metric("bldm_consistency", bldm.consistency()[0], model_version) # meastures how similar the labels are for similar instanes
            log_metric("bldm_smoothed_edf", bldm.smoothed_empirical_differential_fairness(), model_version) #

            ds_preds = ds.copy()
            ds_preds.labels=preds

            #get fairness metric from classificationmetric. This checks fairness in predictions
            cm = ClassificationMetric(ds, ds_preds, unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
            log_metric("cm_tpr_diff", cm.true_positive_rate_difference(), model_version) 
            log_metric("cm_selection_rate", cm.selection_rate(), model_version) 
            log_metric("cm_theil_index", cm.theil_index(), model_version) 
            log_metric("cm_false_positive_rate_ratio", cm.false_positive_rate_ratio(), model_version) 
            log_metric("cm_false_omission_rate_ratio", cm.false_omission_rate_ratio(), model_version) 
            log_metric("cm_false_negative_rate_ratio", cm.false_negative_rate_ratio(), model_version)
            log_metric("cm_false_discovery_rate_ratio", cm.false_discovery_rate_ratio(), model_version) 
            log_metric("cm_error_rate_ratio", cm.error_rate_ratio(), model_version)  
            log_metric("cm_differential_fba", cm.differential_fairness_bias_amplification(), model_version)
           
           #TODO: we should have bias thresholds, and if any are exceeded, then we can reweigh the dataset
           #via something like: https://aif360.readthedocs.io/en/stable/modules/generated/aif360.algorithms.preprocessing.Reweighing.html
           #will have to think about how this applies in the workflow though.
           #i.e. we may want to move the dataset bias stuff up in the data_processing step. 


def get_deployed_model_version(model_version, continual_run, model=None): 
    if model is None: 
        model = continual_run.models.get(model_version.parent)

    current_deployed_version = model.current_version 

    if len(current_deployed_version) == 0: #if no deployed version, look at last mv trained
        current_deployed_version = model.latest_model_version

    current_deployed_model_verison = None 
    if len(current_deployed_version) > 0: 
        current_deployed_model_verison = model.model_versions.get(current_deployed_version)

    return current_deployed_model_verison
    
def get_model_from_dvc(experiment, config): 
    algo = experiment.metadata.get(key="algorithm").data.replace('"','') 
    hexsha = experiment.tags.get("git_hexsha").value
    model_version_id = experiment.parent.split("/")[-1]
    model_path = "model/%s/%s/%s" %(dvc_path, model_version_id, algo, experiment.id)  

    _,_ = execute_cmd("dvc get %s %s/%s --rev %s -o %s" %(os.getcwd(), config.get("DVC_DIR"), model_path, hexsha, model_path))
    model = joblib.load(model_path)
    return model 

def get_winning_experiment_from_model_version(model_version): 
    #might need to repull model_verison here to get updated info 
    experiment_name = model_version.metadata.get(key="winning_experiment_name").data.replace('"','')
    experiment = model_version.experiments.get(experiment_name)

    return experiment

def get_model_obj(model_version, config, type=None): 
    #get winning experiment for the mv 
    experiment = get_winning_experiment_from_model_version(model_version)

    if type == None:
        type = experiment.tags.get(key="storage_type").value 

    if type == "continual": 
        artifact = experiment.artifacts.get(key="model_artifact")
        os.makedirs(artifact.id, exist_ok = True)
        _, download_path = artifact.download(dest_dir = artifact.id)
        model = joblib.load(download_path)

    elif type == "dvc":
        model = get_model_from_dvc(experiment, config)

    return model 

def compare_model_performance(model, deployed_model, data, perf_metric, algo, current_model_version): 
    current_predictions = get_predictions(model, data, algo)
    deployed_predictions = get_predictions(deployed_model, data, algo)

    current_metrics = calculate_metrics(data, current_predictions, [perf_metric], problem_type="classification")
    deployed_metrics = calculate_metrics(data, deployed_predictions, [perf_metric], problem_type="classification")

    is_new_model_better, metric_diff = get_metric_comparison(deployed_metrics, current_metrics, perf_metric)

    log_metric("deployed_model_perf_metric_diff", metric_diff, current_model_version)

    return is_new_model_better, metric_diff

#need to refactor this w/ model checks
def calculate_model_drift(model, deployed_model, data, algo, model_version, config, type):
    df_current = data["X_test"].copy() 
    df_deployed = df_current.copy()

    if type=="continual": 
        #todo -- need to refactor internal model check code 
        pass

    elif type =="evidently": 
        column_mapping = ColumnMapping()
        column_mapping.target=config.get("MODEL_TARGET")
        column_mapping.prediction="prediction"
        df_current["prediction"] = model.predict(df_current)
        df_deployed["prediction"] = deployed_model.predict(df_deployed)

        classification_test = TestSuite(tests=[TestColumnDrift(column_name="prediction")])

        classification_test.run(current_data=df_current, reference_data=df_deployed, column_mapping=column_mapping)
        file_path = "%s/EVIDENTLY_CLASSIFICATION_MODEL_DRIFT_REPORT.HTML" %os.getcwd()
        classification_test.save_html(file_path)
        artifact = model_version.artifacts.create(key="model_drift_report", path = file_path, type = "html", external = False)
        
def build_model_lineage(model_version, dataset_versions): 

    for dv in dataset_versions: 
        dv.assignments.create(resource_name=model_version.name)
        #when supported, we should add assignments to other things we want to track: <code>.py, requirements.txt, docker containers, etc
    
    # turn datasets into a dict and save
    # we're doing this so from mv we can reference all datasets used. 
    # This is useful when we want to be able to retrieve training data used later on
    dataset_arr = [dv.name for dv in dataset_versions]
    dataset_dict = {x:y for x,y in zip(range(len(dataset_arr)),dataset_arr)}
    model_version.metadata.create(key="dataset_versions", data=dataset_dict)

def retrain_model_on_all_data(model_version, data, config, continual_run, version_type=None): 
    has_test = ("X_test" in data.keys())
    
    df_X = pd.concat([data["X_train"], data["X_valid"]])
    df_y = pd.concat([data["y_train"], data["y_valid"]])

    if has_test: 
        df_X = pd.concat([df_X, data["X_test"]])
        df_y = pd.concat([df_y, data["y_test"]])

    train_data = {"X_train" : df_X, "y_train": df_y}
    winning_experiment = get_winning_experiment_from_model_version(model_version)
    params = json.loads(winning_experiment.metadata.get(key = "training_params").data)
    algo = winning_experiment.metadata.get(key = "algorithm").data.replace('"','')

    model, exp = build_model(train_data, config, algo, params, model_version, version_type)                
    #only have a training set so these are not really useful
    ##predictions = get_predictions(model, train_data, algo)
    ##metrics_val = calculate_metrics(train_data, predictions, metrics)
    ##log_metrics(exp, metrics_val, perf_metric)
    ##model_version.create_metrics(metrics=winning_exp.list_metrics())
    
    #none of these below are updateable right now, revisit once the pr gets in. 
    #model_version.performance_metric_name = winning_exp.performance_metric_name
    #model_version.performance_metric_value = winning_exp.performance_metric_val
    #model_version.experiment_name = winning_exp.name
    model_version.metadata.create(key="winning_experiment_name", data=exp.name) #update? 

    return model, exp

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
