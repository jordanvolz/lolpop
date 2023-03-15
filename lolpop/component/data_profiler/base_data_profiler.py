from lolpop.component.abstract_component import AbstractComponent

class BaseDataProfiler(AbstractComponent): 

    def profile_data(self, data, *args, **kwargs): 
        pass 

    def compare_data(self, data, prev_data, *args, **kwargs): 
        pass
