from lolpop.component.logger.base_logger import BaseLogger
from colorama import init as colorama_init, Fore, Style
from datetime import datetime 
class StdOutLogger(BaseLogger): 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        colorama_init()
        
    def log(self, msg, level, time=None, process_name=None, line_num=None, *args, **kwargs): 
        if self._get_level_value(level) <= self._get_level_value(self._get_config("log_level", "DEBUG")):
            msg_out = ""
            if not time:
                formatted_level = self._get_level_format(level)
                time = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S.%f")
            msg_out = msg_out + "%s [%s] " % (time, formatted_level)
            if process_name: 
                msg_out = msg_out + "<%s%s%s" %(Fore.BLUE,process_name,Style.RESET_ALL)
                if line_num and self._get_config("use_line_numbers",False): 
                    msg_out = msg_out + \
                        "|%s%s%s> ::: %s" % (Fore.GREEN, line_num, Style.RESET_ALL,  msg)
                else: 
                    msg_out = msg_out + "> ::: %s" %msg
            print(msg_out)

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


    def _get_level_format(self, level):
        level_num = self._get_level_value(level)
        if level_num < 3:
            return "%s%s%s" % (Fore.RED, level, Style.RESET_ALL)
        elif level_num == 3:
            return "%s%s%s" % (Fore.YELLOW, level, Style.RESET_ALL)
        else: #>4 = INFO or better 
            return level
