from lolpop.component.base_component import BaseComponent

class BaseTestRecorder(BaseComponent):

    test_results = []

    def record_test(self, obj, method, test, test_method, result, *args, **kwargs):
        pass

    def print_report(*args, **kwargs): 
        pass 

    def generate_report(*args, **kwargs): 
        pass 
