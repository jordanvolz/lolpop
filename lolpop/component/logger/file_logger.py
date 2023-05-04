from lolpop.component.logger.base_logger import BaseLogger
import logging 

class FileLogger(BaseLogger): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filename = self._get_config("filename","lolpop.log")
        level = self._get_config("level", "INFO")
        logging.basicConfig(filename=filename, level=level) 

    def log(self, msg, level): 
        logging.log(level, msg)