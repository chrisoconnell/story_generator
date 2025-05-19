#%%
import pytest
from unittest.mock import Mock
from openai import OpenAI
from story_generator.grok import ask_grok_format, _call_ask_grok, ask_grok, get_model, _models
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from story_generator.messages import Messages


@pytest.fixture
def mock_client():
    """Fixture providing a mock OpenAI client with basic setup"""
    client = Mock(spec=OpenAI)

    # Create mock response structure
    mock_message = Mock(spec=ChatCompletionMessage)
    mock_message.refusal = None
    mock_message.content = "test content"
    mock_choice = Mock()
    mock_completion = Mock(spec=ChatCompletion)

    # Set up the chain
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]

    # Set the completion as the return value for parse method
    client.beta.chat.completions.parse.return_value = mock_completion
    client.chat.completions.create.return_value = mock_completion

    # Store the message mock on the client for easy access in tests
    client.mock_message = mock_message

    return client

@pytest.fixture
def mock_messages():
    messages = Messages()
    messages.add_user_message("test message")

    return messages

@pytest.fixture
def mock_response_format():
    return {"type": "test_format"}


def test_ask_grok_format_successful(mock_client, mock_messages, mock_response_format):
    mock_client.mock_message.parsed = [('field1', 'value1'), ('field2', 'value2')]

    result = ask_grok_format(mock_client, mock_messages, mock_response_format)

    assert isinstance(result, tuple)
    assert result == ('value1', 'value2')
    mock_client.beta.chat.completions.parse.assert_called_once()

def test_ask_grok_format_empty_response(mock_client, mock_messages, mock_response_format):
    mock_client.mock_message.parsed = []

    result = ask_grok_format(mock_client, mock_messages, mock_response_format)

    assert isinstance(result, tuple)
    assert result == ()

@pytest.mark.parametrize("error_class", [
    ValueError,
    TypeError,
    Exception
])
def test_ask_grok_format_error_handling(error_class, mock_client, mock_messages, mock_response_format):
    mock_client.beta.chat.completions.parse.side_effect = error_class("Test error")

    result = ask_grok_format(mock_client, mock_messages, mock_response_format)
    assert isinstance(result, tuple)
    assert result == (None, None)

def test_call_ask_grok(mock_client, mock_messages):
    result = _call_ask_grok(mock_client, mock_messages)
    assert isinstance(result, ChatCompletionMessage)

def test_ask_grok(mock_client, mock_messages):
    result = ask_grok(mock_client, mock_messages)
    assert isinstance(result, str)

def test_ask_grok_catch_exception(mock_client, mock_messages):
    mock_client.chat.completions.create.side_effect = Exception("Test error")
    result = ask_grok(mock_client, mock_messages)
    assert result == ''

def test_ask_grok_handle_refusal(mock_client, mock_messages):
    mock_client.mock_message.refusal = "test refusal"
    result = ask_grok(mock_client, mock_messages)
    assert result == ''

def test_get_model():
    result = get_model()
    assert result == _models["default"]

    result = get_model("wrong model")
    assert result == _models["default"]

    result = get_model("fast")
    assert result == _models["fast"]