from component.abstract_component import AbstractComponent

class AbstractDataTransformer(AbstractComponent): 

    def get_data(self, **kwargs): 
        pass 

    def transform(self, data, **kwargs):
        pass