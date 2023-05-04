from lolpop.component.base_component import BaseComponent


class BaseDataConnector(BaseComponent):

    def get_data(self, source, *args, **kwargs):
        pass

    def save_data(self, data, target, *args, **kwargs):
        pass
