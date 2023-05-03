from lolpop.pipeline.abstract_pipeline import AbstractPipeline

class BaseWrapper(AbstractPipeline):
    def __init__(self, conf, runner_conf, pipeline_type="wrapper", **kwargs):
        super().__init__(conf, runner_conf, pipeline_type=pipeline_type, **kwargs)

    def run(self, *args, **kwargs):
        pass