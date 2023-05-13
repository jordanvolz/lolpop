from lolpop.component.genai_chatbot.base_genai_chatbot import BaseGenAIChatbot
from lolpop.utils import common_utils as utils

import openai

class OpenAIChatbot(BaseGenAIChatbot):

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.api_key = utils.load_config(["OPENAI_API_KEY"], self.config).get("OPENAI_API_KEY")

    def ask(self, messages=[], model="gpt-3.5-turbo", **kwargs):
    
        if len(messages) == 0: 
            raise Exception("Error: No messages provided to chatbot. Please try again with non-null content.")
        else: 
            completion = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                **kwargs
            )

            return completion.choices[0].message.content
        
    def prepare_message(self, role=None, content=None, *args, **kwargs): 
        return {"role": role, "content": content}
