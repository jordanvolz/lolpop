from lolpop.component.logger.base_logger import BaseLogger
from colorama import init as colorama_init, Fore, Style
from datetime import datetime 
class StdOutLogger(BaseLogger): 
    

    __DEFAULT_CONF__ = {"config": {"log_level": "DEBUG", "use_line_numbers": False}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        colorama_init()
        
    def log(self, msg, level, time=None, process_name=None, line_num=None, *args, **kwargs): 
        """
        Logs the message to standard output.

        Args:
            msg (str): The message to be logged.
            level (str): The level of logging for the message.
            time (str, optional): The timestamp for the message (default=None).
            process_name (str, optional): The name of the process (default=None).
            line_num (int, optional): The line number of the message (default=None).
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            None.
        """
        if self._get_level_value(level) <= self._get_level_value(self._get_config("log_level")):
            msg_out = ""
            if not time:
                formatted_level = self._get_level_format(level)
                time = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S.%f")
            msg_out = msg_out + "%s [%s] " % (time, formatted_level)
            if process_name: 
                msg_out = msg_out + "<%s%s%s" %(Fore.BLUE,process_name,Style.RESET_ALL)
                if line_num and self._get_config("use_line_numbers"): 
                    msg_out = msg_out + \
                        "|%s%s%s> ::: %s" % (Fore.GREEN, line_num, Style.RESET_ALL,  msg)
                else: 
                    msg_out = msg_out + "> ::: %s" %msg
            else: 
                msg_out = msg_out + "::: msg"
            print(msg_out)

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


    def _get_level_format(self, level):
        """
        Returns the level formatted with color codes.

        Args:
            level (str): The level of logging.
        Returns:
            The level formatted with color codes according to its level of severity.
        """
        level_num = self._get_level_value(level)
        if level_num < 3:
            return "%s%s%s" % (Fore.RED, level, Style.RESET_ALL)
        elif level_num == 3:
            return "%s%s%s" % (Fore.YELLOW, level, Style.RESET_ALL)
        else: #>4 = INFO or better 
            return level
