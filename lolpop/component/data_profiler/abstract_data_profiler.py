from lolpop.component.abstract_component import AbstractComponent

class AbstractDataProfiler(AbstractComponent): 

    def profile_data(self, data, **kwargs): 
        pass 

    def compare_data(self, data, prev_data, **kwargs): 
        pass
