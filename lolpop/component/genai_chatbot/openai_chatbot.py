from lolpop.component.genai_chatbot.base_genai_chatbot import BaseGenAIChatbot
from lolpop.utils import common_utils as utils

import openai

class OpenAIChatbot(BaseGenAIChatbot):

    __REQUIRED_CONF__= {"config": ["OPENAI_API_KEY"]}

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.api_key = utils.load_config(["OPENAI_API_KEY"], self.config).get("OPENAI_API_KEY")

    def ask(self, messages=[], model="gpt-3.5-turbo", *args, **kwargs):
        """
        Sends a chat message(s) to OpenAI's Chat API and returns the response.

        Args:
            messages (list): A list of strings representing the messages to send to the chatbot. Default is an empty list.
            model (str): A string representing the name of the model to use for generating chat responses. Default is "gpt-3.5-turbo".
            **kwargs: Arbitrary keyword arguments representing the additional options to pass to the Chat API.

        Returns:
            A string representing the generated chatbot response.

        Raises:
            Exception: If no messages are provided to the chatbot.
        """
        if len(messages) == 0: 
            raise Exception("Error: No messages provided to chatbot. Please try again with non-null content.")
        else: 
            completion = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                **kwargs
            )

            return completion.choices[0].message.content
        
    def prepare_message(self, role="user", content=None, *args, **kwargs): 
        """
        Prepares a chat message with the specified role and content.

        Args:
            role (str): A string representing the role of the person sending the message. Default is "user".
            content (str): A string representing the content of the message to be sent. Default is None.

        Returns:
            A dictionary representing the prepared message with the specified role and content.
        """
        return {"role": role, "content": content}
