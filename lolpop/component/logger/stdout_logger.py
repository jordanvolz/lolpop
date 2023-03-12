from lolpop.component.logger.abstract_logger import AbstractLogger

class StdOutLogger(AbstractLogger): 
    
    def __init__(self, config, *args, **kwargs):
        pass
        
    def log(self, msg, level): 
        print(msg)