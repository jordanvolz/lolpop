from pipeline.abstract_pipeline import AbstractPipeline 

class AbstractProcess(AbstractPipeline): 

    datasets_used = []

    def __init__(self, conf, runner_conf, pipeline_type = "process", **kwargs):
        super().__init__(conf, runner_conf, **kwargs)

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

