from component.model_deployer.abstract_model_deployer import AbstractModelDeployer
from utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class SeldonModelDeployer(AbstractModelDeployer): 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    def deploy_model(self, model, *args, **kwargs): 
        pass 

    def build_api(self, model, *args, **kwargs): 
        pass 

    def build_container(self, model, *args, **kwargs): 
        pass 

    def package_model(self, model, *args, **kwargs): 
        pass