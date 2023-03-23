from lolpop.component.resource_version_control.abstract_resource_version_control import AbstractResourceVersionControl
from lolpop.component.metadata_tracker.wandb_metadata_tracker import WandBMetadataTracker
from lolpop.utils import common_utils as utils
import wandb
import os
import joblib
import pandas as pd
import glob

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class WandBVersionControl(AbstractResourceVersionControl): 
    __REQUIRED_CONF__ = {
        "config" : ["local_dir"]
    }
    def __init__(self, conf, pipeline_conf, runner_conf, description=None, run_id=None, components = {}, **kwargs): 
        #set normal config
        super().__init__(conf, pipeline_conf, runner_conf, components=components, **kwargs)
        
        # if we are using continual for metadata tracking then we won't have to set up connection to continual
        # if not, then we do. If would be weird to have to do this, but just in case. 
        if isinstance(components.get("metadata_tracker"), WandBMetadataTracker): 
            self.client = self.metadata_tracker.client
            self.run = self.metadata_tracker.run
        else: 
            secrets = utils.load_config(
                "WANDB_KEY", "WANDB_PROJECT", "WANDB_ENTITY", conf.get("config", {}))
            self.client = wandb
            wandb.login(key=secrets.get("WANDB_KEY", "WANDB_PROJECT"))
            self.run = wandb.init(
                project=secrets.get("WANDB_PROJECT"), id=run_id)

    def version_data(self, resource, data, key = "data_csv", **kwargs): 
        #id = dataset_version.name.split(":")[0]
        id = resource(0)
        type = resource(1)

        #dump dataframe to local
        local_path = "%s/%s_%s.csv" %(self.config.get("local_dir"),id, key)
        data.to_csv(local_path, index=False)

        self.metadata_tracker.log_artifact(id, path = local_path, key=key, type=type, external=False)
        
        return {"uri" : None}

    def get_data(self, artifact, vc_info=None, key="data_csv", **kwargs):
        name, version = artifact.name.split(":")
        file_path = "%s/%s/%s" %(self._get_config("local_dir"),name, version)
        os.makedirs(file_path, exist_ok=True)
        download_path = artifact.download(file_path)
        csv_files = glob.glob(os.path.join(download_path, "*.csv"))
        pd_arr = []
        for file in csv_files: 
            df = pd.read_csv(file)
            pd_arr.append(df)
        df = pd.concat(pd_arr, axis=1)
        return df

    def version_model(self, experiment, model, algo, **kwargs): 
        id = self.metadata_tracker.get_resource_id(experiment)

        model_dir = "%s/models/%s" %(self._get_config("local_dir"), algo)    
        os.makedirs(model_dir, exist_ok=True)
        model_path = "%s/%s" %(model_dir, id)
        joblib.dump(model, model_path)
        artifact = self.metadata_tracker.log_artifact(experiment, id = "model_artifact", path=model_path, external=False)

        return {"uri" : artifact.url}
    
    def get_model(self, experiment, key="model_artifact", **kwargs): 
        artifact = self.metadata_tracker.get_artifact(experiment,id=key)
        file_path = "%s/%s" %(self._get_config("local_dir"),experiment.id)
        os.makedirs(file_path, exist_ok=True)
        _, download_path = artifact.download(dest_dir=file_path)
        model = joblib.load(download_path)
        
        return model 
 