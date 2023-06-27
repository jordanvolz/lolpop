from lolpop.component.base_component import BaseComponent

class BaseLogger(BaseComponent): 

    url = None

    def log(self, msg, level): 
        pass 