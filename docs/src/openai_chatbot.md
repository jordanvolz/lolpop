# OpenAIChatbot

The `OpenAIChatbot` class is a Python class that provides methods for interacting with OpenAI's Chat API to generate chatbot responses for given messages. This class is a subclass of the `BaseGenAIChatbot` base class. In this documentation, we will describe the methods of this class in detail.


## Configuration

### Required Configuration
The OpenAI chatbot requires the following configuration: 

- `openai_api_key`: API key for OpenAI. 

### Optional Configuration
The OpenAI chatbot  has no optional configuration.

### Default Configuration
The OpenAI chatbot has not default configuration.

## Methods

### ask 
This method generates a chatbot response for the given messages using OpenAI's Chat API. It takes a list of `messages` as input which represent the messages to be sent to the chatbot and returns a string representing the generated chatbot response. This method raises an exception if no messages are provided to the chatbot.

```python 
def ask(self, messages=[], model="gpt-3.5-turbo", *args, **kwargs)
```

**Arguments**: 

* `messages` (list): A list of strings representing the messages to send to the chatbot. Default is an empty list.
* `model` (str): A string representing the name of the model to use for generating chat responses. Default is "gpt-3.5-turbo".

**Returns**: 

* A string representing the generated chatbot response


### prepare_message 

This method prepares a chat message with the specified role and content and returns it as a dictionary.


```python 
def prepare_message(self, role="user", content=None, *args, **kwargs)
```

**Arguments**: 

* `role` (str): A string representing the role of the person sending the message. Default is "user".
* `content` (str): A string representing the content of the message to be sent. Default is None.

**Returns##: 

* A dictionary representing the conversation including `role` and `content`

## Usage

```python
from lolpop.component import OpenAIChatbot

config = {
    #insert component config here 
}

openai_chatbot = OpenAIChatbot(conf=config)

prompts = [openai_chatbot.prepare_message(content="Hi, how are you?")]

response = openai_chatbot.ask(messages=prompts)
print(response)
```