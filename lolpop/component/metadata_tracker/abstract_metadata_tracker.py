from lolpop.component.abstract_component import AbstractComponent

class AbstractMetadataTracker(AbstractComponent): 

    url: str = "https://replace.me"

    def log_artifact(self, resource, **kwargs): 
        pass 

    def get_artifact(self, resource, id, **kwargs):
        pass

    def log_tag(self, resource, **kwargs): 
        pass
    
    def get_tag(self, resource, key, **kwargs): 
        pass

    def log_metadata(self, resource, **kwargs): 
        pass 

    def get_metadata(self, resource, key, **kwargs): 
        pass

    def create_resource(self, type, **kwargs): 
        pass

    def get_resource(self, id, type, **kwargs): 
        pass

    def get_resource_id(self, resource, **kwargs): 
        pass 

    def register_vc_resource(self, resource, vc_info, **kwargs): 
        pass

    def log_data_profile(self, resource, **kwargs): 
        pass 
    
    def get_data_profile(self, resource, id, **kwargs): 
        pass 

    def log_checks(self, resource, **kwargs): 
        pass 
    
    def get_data_checks(self, resource, id, **kwargs): 
        pass 

    def stop(self): 
        pass
    