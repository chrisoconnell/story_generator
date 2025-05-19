import os
from openai import OpenAI, NotGiven
from dotenv import load_dotenv
from openai.lib import ResponseFormatT
from openai.types.chat import ChatCompletionMessage
from story_generator.decorators import retry_on_parse_error, catch_exception
from typing import Union, Type

from story_generator.messages import Messages

load_dotenv()

_models = {
    "base": "grok-3",
    "fast": "grok-3-fast",
    "cheap": "grok-2-1212",
    "default": "grok-2-1212"
}

def get_model(model: str = None) -> str:
    return _models.get(model, _models["default"])

def get_client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )

@retry_on_parse_error()
def ask_grok_format(
        client: OpenAI,
        messages: Messages,
        response_format: Union[Type[ResponseFormatT], NotGiven]
) -> tuple:
    completion = client.beta.chat.completions.parse(
        model=get_model(),
        response_format=response_format,
        messages=messages.messages,
    )

    parsed_values = completion.choices[0].message.parsed
    return tuple(value[1] for value in parsed_values)

@catch_exception
def ask_grok(client: OpenAI, messages: Messages) -> str:
    message = _call_ask_grok(client, messages)
    if message.refusal is not None:
        raise Exception(f"Grok API refused to respond: {message.refusal}")

    return message.content

def _call_ask_grok(client: OpenAI, messages: Messages) -> ChatCompletionMessage:
    completion = client.chat.completions.create(
        model=get_model(),
        messages=messages.messages,
    )

    return completion.choices[0].message

