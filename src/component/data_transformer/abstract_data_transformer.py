from component.abstract_component import AbstractComponent

class AbstractDataTransformer(AbstractComponent): 

    def get_data(self, *args, **kwargs): 
        pass 

    def transform(self, data, *args, **kwargs):
        pass

    def save_data(self, data, *args, **kwargs):
        pass