from lolpop.pipeline.base_pipeline import BasePipeline

class BasePredict(BasePipeline): 
    def __init__(self, pipeline_type="predict", *args, **kwargs):
        super().__init__(pipeline_type=pipeline_type, *args, **kwargs)
