from pipeline.predict.abstract_predict import AbstractPredict
from utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class OfflinePredict(AbstractPredict): 
    pass