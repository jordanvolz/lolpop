from lolpop.component.base_component import BaseComponent

class BaseResourceVersionControl(BaseComponent): 

    def version_data(self, id, data, *args, **kwargs): 
        pass 

    def get_data(self, id, *args, **kwargs):
        pass

    def version_model(self, id, model, *args, **kwargs): 
        pass
    
    def get_model(self, id, *args, **kwargs): 
        pass
