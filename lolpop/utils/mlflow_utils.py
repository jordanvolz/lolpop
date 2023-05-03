import mlflow
from mlflow.tracking import MlflowClient
from functools import wraps 

def get_client(tracking_uri):
    mlflow.set_tracking_uri(tracking_uri)

    return MlflowClient(tracking_uri=mlflow.get_tracking_uri())

def get_experiment(experiment_name):

    try:
        experiment = mlflow.get_experiment_by_name(experiment_name)
        experiment_id = experiment.experiment_id
    except:
        experiment_id = mlflow.create_experiment(experiment_name)

    return experiment_id

def create_run(client, experiment_id): 
    #use mlflow.start_run instead of client.create_run because the latter doesn't set the active run
    run = mlflow.start_run(experiment_id=experiment_id)
    #run = client.create_run(experiment_id=experiment_id)
    #tag as a parent run for filtering on previous runs
    client.set_tag(run.info.run_id, "parent_run", "True")
    return run 

def create_nested_run(parent_run): 
    active_run = mlflow.active_run()
    #make sure we have the right active run
    #Note that if you start_run for an already active_run you get an error from mlflow 
    if active_run is not None: 
        #if the parent is not the active run, make it the active run so the nested run
        #is properly placed under the parent run
        if active_run.info.run_id != parent_run.info.run_id: 
            mlflow.start_run(run_id = parent_run.info.run_id)
    else: #we have no active run, so we ened ot start the parent run
        mlflow.start_run(run_id=parent_run.info.run_id)
    #create nested run under parent
    run = mlflow.start_run(experiment_id=parent_run.info.experiment_id, nested=True)
    return run 

def stop_run(run_id, experiment_id): 
    mlflow.end_run()
    #if we were in a nested run then we should end the parent run too. 
    active_run = mlflow.active_run()
    if active_run is not None: 
        mlflow.end_run()

def connect(tracking_uri, experiment_name):
    client = get_client(tracking_uri)
    experiment_id = get_experiment(experiment_name)
    run = create_run(client, experiment_id) 

    return client, run

def get_run(client, run_id): 
    run = client.get_run(run_id)
    return run

#wraps logging calls around function execution
# This decorator can be used to make sure mlflow has the right active run for the object
# used. Typically, obj here will be metadata_tracker, metrics_tracker, model_respository, etc. 
# This is needed because many mlflow command live under mflow and not the mlflow client, so that when you
# are executing complex workflows, mlflow won't know what the active run is if it's being spun up in anothe process
# this was discovered when testing mlflow w/ metaflow pipelines, but it's a good thing to safeguard against in general
def check_active_mlflow_run(mlflowlib):
    def check_decorator(func):
        @wraps(func)
        def wrapper(obj, *args, **kwargs):
            if mlflowlib.active_run() is None:
                run_id = obj.run.info.run_id
                uri = obj.url
                obj.log("No active mlflow run found. Reinitializing with saved values: run id %s with uri %s" %(run_id, uri))
                mlflowlib.set_tracking_uri(uri)
                mlflowlib.start_run(run_id=run_id)
            return func(obj, *args, **kwargs)
        return wrapper
    return check_decorator
