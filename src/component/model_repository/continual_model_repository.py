from component.model_repository.abstract_model_repository import AbstractModelRepository
from utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class ContinualModelRepository(AbstractModelRepository): 
    __REQUIRED_CONF__ = {
        "components" : ["metadata_tracker|ContinualMetadataTracker"],
        "config" : []
    }
    def register_model(self, model, *args, **kwargs): 
        pass 

    def promote_model(self, model, *args, **kwargs): 
        pass 

    def approve_model(self, model, *args, **kwargs): 
        pass 