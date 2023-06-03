from lolpop.runner.classification_runner.classification_runner import ClassificationRunner
from lolpop.utils import common_utils as utils


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class RegressionRunner(ClassificationRunner):

    def __init__(self, problem_type="regression", *args, **kwargs):
        super().__init__(problem_type=problem_type, *args, **kwargs)