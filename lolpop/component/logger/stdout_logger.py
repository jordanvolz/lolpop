from lolpop.component.logger.base_logger import BaseLogger
class StdOutLogger(BaseLogger): 
    
    #def __init__(self, config, *args, **kwargs):
    #    super().__init__(config, *args, **kwargs)
        
    def log(self, msg, level): 
        if self._get_level_value(level) <= self._get_level_value(self._get_config("log_level", "DEBUG")):
            print(msg)

    def _get_level_value(self, level): 
        if level == "NONE": 
            return 0 
        elif level == "FATAL":
            return 1 
        elif level == "ERROR": 
            return 2
        elif level == "WARN" or level == "WARNING": 
            return 3
        elif level == "INFO": 
            return 4 
        elif level == "DEBUG": 
            return 5 
        elif level == "TRACE": 
            return 6 
        elif level == "ALL": 
            return 100 