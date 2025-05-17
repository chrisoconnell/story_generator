#%%
import pytest
from unittest.mock import Mock, patch
from openai import OpenAI
from story_generator.grok import ask_grok_format
from openai.types.chat import ChatCompletion, ChatCompletionMessage


@pytest.fixture
def mock_client():
    """Fixture providing a mock OpenAI client with basic setup"""
    client = Mock(spec=OpenAI)

    # Create mock response structure
    mock_message = Mock(spec=ChatCompletionMessage)
    mock_choice = Mock()
    mock_completion = Mock(spec=ChatCompletion)

    # Set up the chain
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]

    # Set the completion as the return value for parse method
    client.beta.chat.completions.parse.return_value = mock_completion

    # Store the message mock on the client for easy access in tests
    client.mock_message = mock_message

    return client


def test_ask_grok_format_successful(mock_client):
    mock_client.mock_message.parsed = [('field1', 'value1'), ('field2', 'value2')]

    messages = [{"role": "user", "content": "test message"}]
    response_format = {"type": "test_format"}

    result = ask_grok_format(mock_client, messages, response_format)

    assert isinstance(result, tuple)
    assert result == ('value1', 'value2')
    mock_client.beta.chat.completions.parse.assert_called_once()

def test_ask_grok_format_empty_response(mock_client):
    mock_client.mock_message.parsed = []

    messages = [{"role": "user", "content": "test message"}]
    response_format = {"type": "test_format"}

    result = ask_grok_format(mock_client, messages, response_format)

    assert isinstance(result, tuple)
    assert result == ()

@pytest.mark.parametrize("error_class", [
    ValueError,
    TypeError,
    Exception
])
def test_ask_grok_format_error_handling(error_class, mock_client):
    mock_client.beta.chat.completions.parse.side_effect = error_class("Test error")

    messages = [{"role": "user", "content": "test message"}]
    response_format = {"type": "test_format"}

    result = ask_grok_format(mock_client, messages, response_format)
    assert isinstance(result, tuple)
    assert result == (None, None)
