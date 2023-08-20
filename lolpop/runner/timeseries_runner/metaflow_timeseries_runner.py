from lolpop.runner.classification_runner.metaflow_classification_runner import MetaflowClassificationRunner
from lolpop.utils import common_utils as utils


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class MetaflowTimeSeriesRunner(MetaflowClassificationRunner):

    def __init__(self, problem_type="timeseries", *args, **kwargs):
        super().__init__(problem_type=problem_type, *args, **kwargs)
