from lolpop.pipeline.base_pipeline import BasePipeline

class BaseWrapper(BasePipeline):
    def __init__(self, pipeline_type="wrapper", *args, **kwargs):
        super().__init__(pipeline_type=pipeline_type, *args, **kwargs)

    def run(self, *args, **kwargs):
        pass