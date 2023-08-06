## Overview

A `genai_chatbot` is a component that is able to communicate with an LLM chatbot to ask questions and retrieve text responses. The main intention of this component is to be utilized in [cli](cli.md) applications which want to make use of generative AI. 

## Attributes

`BaseGenAIChatbot` contains no default attributes. 

## Configuration

`BaseGenAIChatbot` contains no default or required configuration. 


## Interface

The following methods are part of `BaseGenAIChatbot` and should be implemented in any class that inherits from this base class: 

### ask

Sends a prompt to the LLM and retrieves a response. 

```python
def ask(self, prompt, *args, **kwargs) -> str
```

**Arguments**: 

- `prompt` (list(str)): The text prompts to send to the chatbot.   

**Returns**:

- `response` (str): A text response from the chatbot.  

### prepare_message

Prepares a prompt prior to sending it to the LLM. Many LLMs may benefit from providing some history or context to a conversation, or you may wish to chain responses together to have an interactive conversation.  

```python
def prepare_mesasge(self, role, content, *args, **kwargs) -> dict[str, Any]
```

**Arguments**: 

- `role` (str): The role you wish the LLM to assume during the conversation. 
- `content` (str): The content to include in the conversation. 

**Returns**:

- `dict` (str, Any): A dictionary representing the conversation history
