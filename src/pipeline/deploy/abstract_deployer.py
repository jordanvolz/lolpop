from pipeline.abstract_pipeline import AbstractPipeline 

class AbstractProcess(AbstractPipeline): 

    def promote_model(self, model_version, *args, **kwargs): 
        pass 

    def deploy_model(self, model_version, *args, **kwaargs): 
        pass 

    def approve_model(self, model_version, *args, **kwargs): 
        pass 