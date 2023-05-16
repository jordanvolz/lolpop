from lolpop.component.logger.base_logger import BaseLogger
import logging 
from datetime import datetime 
class FileLogger(BaseLogger): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filename = self._get_config("log_filename","lolpop.log")
        level = self._get_config("log_level", "INFO")
        logging.basicConfig(filename=filename, level=level) 

    def log(self, msg, level, time = None, process_name=None, line_num=None, *args, **kwargs): 
        if self._get_level_value(level) <= self._get_level_value(self._get_config("log_level", "DEBUG")):
            msg_out = ""
            if not time:
                time = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S.%f")
            msg_out = msg_out + "%s [%s] " % (time, level)
            if process_name:
                msg_out = msg_out + \
                    "<%s" % (process_name)
                if line_num and self._get_config("use_line_numbers", False):
                    msg_out = msg_out + \
                        "|%s> ::: %s" % (
                            line_num, msg)
                else:
                    msg_out = msg_out + "> ::: %s" % msg
            logging.log(level, msg, **kwargs)

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
