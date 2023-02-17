from component.abstract_component import AbstractComponent

class AbstractResourceVersionControl(AbstractComponent): 

    def version_data(self, id, data, *args, **kwargs): 
        pass 

    def get_data(self, id, *args, **kwargs):
        pass

    def version_model(self, id, model, *args, **kwargs): 
        pass
    
    def get_model(self, id, *args, **kwargs): 
        pass
