from lolpop.component.logger.abstract_logger import AbstractLogger
import logging 

class FileLogger(AbstractLogger): 

    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        filname = self_get_config("filename") or "mlops-jumpstart.log"
        level = self._get_config("level") or "INFO"
        logging.basicConfig(filename=filename, level=level) 

    def log(self, msg, level): 
        logging.log(level, msg)