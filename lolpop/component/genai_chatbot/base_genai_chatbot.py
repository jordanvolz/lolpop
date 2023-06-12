from lolpop.component.base_component import BaseComponent


class BaseGenAIChatbot(BaseComponent):

    def ask(self, prompt, *args, **kwargs):
        pass

    def prepare_message(self, role, content, *args, **kwargs): 
        pass