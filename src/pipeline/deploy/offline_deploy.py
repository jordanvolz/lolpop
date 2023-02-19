from pipeline.deploy.abstract_deploy import AbstractDeploy
from utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class OfflineDeploy(AbstractDeploy): 

    def __init__(self, conf, runner_conf, **kwargs): 
        super().__init__(conf, runner_conf, **kwargs)

    def promote_model(self, model_version, *args, **kwargs): 
        pass 

    def deploy_model(self, model_version, *args, **kwaargs): 
        pass 

    def approve_model(self, model_version, *args, **kwargs): 
        pass 