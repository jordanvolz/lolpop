from lolpop.pipeline.base_pipeline import BasePipeline
from typing import Any 

class BaseDeploy(BasePipeline): 
    def __init__(self,pipeline_type="deploy", *args, **kwargs):
        super().__init__(pipeline_type=pipeline_type, *args, **kwargs)

    def promote_model(self, model_version, *args, **kwargs) -> Any: 
        pass 

    def deploy_model(self, promotion, *args, **kwaargs) -> Any: 
        pass 

    def approve_model(self, promotion, *args, **kwargs) -> Any: 
        pass 

    def check_approval(self, promotion, *args, **kwargs) -> bool: 
        pass