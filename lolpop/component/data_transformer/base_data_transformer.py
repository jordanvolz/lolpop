from lolpop.component.abstract_component import AbstractComponent

class BaseDataTransformer(AbstractComponent): 

    def get_data(self, source_table_name, *args, **kwargs): 
        pass 

    def transform(self, data, *args, **kwargs):
        pass

    def save_data(self, data, *args, **kwargs):
        pass