from lolpop.component.base_component import BaseComponent

class BaseTestRecorder(BaseComponent):

    def record_test(self, obj, func, result, msg, *args, **kwargs):
        pass

    def print_report(*args, **kwargs): 
        pass 

    def generate_report(*args, **kwargs): 
        pass 
