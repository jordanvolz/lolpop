import mlflow
from mlflow.tracking import MlflowClient


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
    if active_run: 
        if active_run.info.run_id != parent_run.info.run_id: 
            mlflow.start_run(run_id = parent_run.info.run_id)
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