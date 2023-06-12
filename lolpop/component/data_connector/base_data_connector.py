from lolpop.component.base_component import BaseComponent


class BaseDataConnector(BaseComponent):

    def get_data(self, source, *args, **kwargs):
        pass

    def save_data(self, data, target, *args, **kwargs):
        pass

    def _load_data(self, query, config, *args, **kwargs): 
        pass

    def _save_data(self, data, config, *args, **kwargs): 
        pass 