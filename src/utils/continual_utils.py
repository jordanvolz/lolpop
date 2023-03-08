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
