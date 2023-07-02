from lolpop.component.logger.base_logger import BaseLogger
import logging 
from datetime import datetime 
class FileLogger(BaseLogger): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filename = self._get_config("log_filename","lolpop.log")
        self.url = filename 
        level = self._get_config("log_level", "INFO")
        if isinstance(level, str):
            level = self._get_level_value(level)
        format = self._get_config("log_format", "%(message)s")

        logger = logging.getLogger("lolpop")
        logger.setLevel(level)
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(format))
        logger.addHandler(file_handler)

        self.logger = logger
        logger.log(30, "\n\n")
        self.log("Initialized logger for lolpop workflow.", level="INFO")

    def log(self, msg, level="INFO", time = None, process_name=None, line_num=None, *args, **kwargs): 
        if self._get_level_value(level) >= self._get_level_value(self._get_config("log_level", "DEBUG")):
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
            else: 
                msg_out = msg_out + "::: %s" % msg
            self.logger.log(self._get_level_value(level), msg_out, **kwargs)

    def _get_level_value(self, level):
        if level == "FATAL" or level == "CRITICAL":
            return 50
        elif level == "ERROR":
            return 40
        elif level == "WARN" or level == "WARNING":
            return 30
        elif level == "INFO":
            return 20
        elif level == "DEBUG" or level == "TRACE":
            return 10
        elif level == "ALL":
            return 1
        else: #level == "NONE" or level == "NOTSET":
            return 0
