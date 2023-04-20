from lolpop.pipeline.abstract_pipeline import AbstractPipeline

class AbstractPredict(AbstractPipeline): 
    def __init__(self, conf, runner_conf, pipeline_type="predict", **kwargs):
        super().__init__(conf, runner_conf, pipeline_type=pipeline_type, **kwargs)
