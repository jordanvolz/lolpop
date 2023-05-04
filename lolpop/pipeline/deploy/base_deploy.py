from lolpop.pipeline.base_pipeline import BasePipeline

class BaseDeploy(BasePipeline): 
    def __init__(self,pipeline_type="deploy", *args, **kwargs):
        super().__init__(pipeline_type=pipeline_type, *args, **kwargs)

    def promote_model(self, model_version, *args, **kwargs): 
        pass 

    def deploy_model(self, model_version, *args, **kwaargs): 
        pass 

    def approve_model(self, model_version, *args, **kwargs): 
        pass 