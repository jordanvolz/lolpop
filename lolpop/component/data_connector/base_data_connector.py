from lolpop.component.abstract_component import AbstractComponent


class BaseDataConnector(AbstractComponent):

    def get_data(self, source, *args, **kwargs):
        pass

    def save_data(self, data, target, *args, **kwargs):
        pass
