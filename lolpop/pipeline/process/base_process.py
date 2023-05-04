from lolpop.pipeline.base_pipeline import BasePipeline

class BaseProcess(BasePipeline): 

    datasets_used = []

    def __init__(self, pipeline_type = "process", *args, **kwargs):
        super().__init__(pipeline_type=pipeline_type, *args, **kwargs)

    def transform_data(): 
        pass 

    def track_data(): 
        pass

    def profile_data(): 
        pass 

    def check_data(): 
        pass 

    def compare_data(): 
        pass 

