from lolpop.component.resource_version_control.base_resource_version_control import BaseResourceVersionControl
from lolpop.component.metadata_tracker.continual_metadata_tracker import ContinualMetadataTracker
from lolpop.utils import common_utils as utils
from lolpop.utils import continual_utils as cutils
import os
import joblib
import pandas as pd

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class ContinualVersionControl(BaseResourceVersionControl): 
    __REQUIRED_CONF__ = {
        "config" : ["local_dir"]
    }
    def __init__(self, description=None, run_id=None, components = {}, *args, **kwargs): 
        #set normal config
        super().__init__(components=components, *args, **kwargs)
        
        # if we are using continual for metadata tracking then we won't have to set up connection to continual
        # if not, then we do. If would be weird to have to do this, but just in case. 
        if isinstance(components.get("metadata_tracker"), ContinualMetadataTracker): 
            self.client = self.metadata_tracker.client
            self.run = self.metadata_tracker.run
        else: 
            secrets = utils.load_config(["CONTINUAL_APIKEY", "CONTINUAL_ENDPOINT", "CONTINUAL_PROJECT", "CONTINUAL_ENVIRONMENT"], self.config)
            self.client = cutils.get_client(secrets)
            self.run = cutils.get_run(self.client, description=description, run_id=run_id)

    def version_data(self, dataset_version, data, key = "data_csv", **kwargs): 
        id = self.metadata_tracker.get_resource_id(dataset_version)

        #dump dataframe to local
        local_path = "%s/%s.csv" %(self.config.get("local_dir"),id)
        data.to_csv(local_path, index=False)

        artifact = self.metadata_tracker.log_artifact(dataset_version, id = key, path = local_path, mime_type="csv", external=False)
        
        return {"uri" : artifact.url}

    def get_data(self, dataset_version, vc_info=None, key="data_csv", **kwargs):
        artifact = dataset_version.artifacts.get(id=key)
        file_path = "%s/%s/%s" %(self._get_config("local_dir"),dataset_version.id, artifact.id)
        os.makedirs(file_path, exist_ok=True)
        _, download_path = artifact.download(dest_dir=file_path)
        df = pd.read_csv(download_path)
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
 