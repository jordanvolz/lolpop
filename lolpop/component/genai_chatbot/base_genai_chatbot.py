from lolpop.component.base_component import BaseComponent
from typing import Any

class BaseGenAIChatbot(BaseComponent):

    def ask(self, prompt, *args, **kwargs) -> str:
        pass

    def prepare_message(self, role, content, *args, **kwargs) -> dict[str,Any]: 
        pass