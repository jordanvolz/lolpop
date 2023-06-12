from lolpop.component.logger.base_logger import BaseLogger
import logging 
from datetime import datetime 
class FileLogger(BaseLogger): 

    __DEFAULT_CONF__ = {"config": {"log_level": "DEBUG", "use_line_numbers": False}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filename = self._get_config("log_filename","lolpop.log")
        level = self._get_config("log_level", "INFO")
        logging.basicConfig(filename=filename, level=level) 

    def log(self, msg, level, time = None, process_name=None, line_num=None, *args, **kwargs): 
        """
        Logs a message using the specified logging level and additional information.

        Args:
            msg (str): Message to be logged.
            level (str): Logging level to use.
            time (datetime, optional): Time to use. Defaults to None.
            process_name (str, optional): Name of the process. Defaults to None.
            line_num(int, optional): Line number associated with message.
                                     Defaults to None.

        Returns:
            None.

        Raises:
            None.
        """
        if self._get_level_value(level) <= self._get_level_value(self._get_config("log_level")):
            msg_out = ""
            if not time:
                time = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S.%f")
            msg_out = msg_out + "%s [%s] " % (time, level)
            if process_name:
                msg_out = msg_out + \
                    "<%s" % (process_name)
                if line_num and self._get_config("use_line_numbers"):
                    msg_out = msg_out + \
                        "|%s> ::: %s" % (
                            line_num, msg)
                else:
                    msg_out = msg_out + "> ::: %s" % msg
            logging.log(level, msg, **kwargs)

    def _get_level_value(self, level):
        """
        Returns the numeric logging level value associated with the specified string level value.

        Args:
            level (str): The string logging level value.

        Returns:
            The corresponding numeric logging level value.

        Raises:
            None.
        """
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
