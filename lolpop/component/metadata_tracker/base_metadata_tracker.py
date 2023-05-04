from lolpop.component.base_component import BaseComponent

class BaseMetadataTracker(BaseComponent): 

    url: str = "https://replace.me"

    def log_artifact(self, resource, *args, **kwargs): 
        pass 

    def get_artifact(self, resource, id, *args, **kwargs):
        pass

    def log_tag(self, resource, *args, **kwargs):
        pass
    
    def get_tag(self, resource, key, *args, **kwargs):
        pass

    def log_metadata(self, resource, *args, **kwargs):
        pass 

    def get_metadata(self, resource, key, *args, **kwargs):
        pass

    def create_resource(self, type, *args, **kwargs):
        pass

    def get_resource(self, id, type, *args, **kwargs):
        pass

    def update_resource(self, resource, updates, *args, **kwargs):
        pass

    def get_prev_resource_version(self, resource_version, *args, **kwargs):
        pass 

    def get_currently_deployed_model_version(self, model_version, *args, **kwargs): 
        pass

    def get_prediction_job_model_version(self, prediction_job, *args, **kwargs): 
        pass 

    def get_latest_model_resource(self, model, type, *args, **kwargs): 
        pass 

    def get_winning_experiment(self, model_version, *args, **kwargs): 
        pass 

    def build_model_lineage(self, model_version, dataset_versions, *args, **kwargs): 
        pass 

    def get_resource_id(self, resource, *args, **kwargs):
        pass 

    def get_parent_id(self, resource, *args, **kwargs): 
        pass 

    def register_vc_resource(self, resource, vc_info, *args, **kwargs):
        pass

    def get_vc_info(self, resource, *args, **kwargs): 
        pass

    def log_data_profile(self, resource, *args, **kwargs):
        pass 
    
    def get_data_profile(self, resource, id, *args, **kwargs):
        pass 

    def log_checks(self, resource, *args, **kwargs):
        pass 
    
    def get_data_checks(self, resource, id, *args, **kwargs):
        pass 

    def log_data_comparison(self, resource, report, *args, **kwargs): 
        pass 

    def stop(self): 
        pass
    