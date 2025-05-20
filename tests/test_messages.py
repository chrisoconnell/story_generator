import json
import unittest.mock
from unittest.mock import mock_open, patch
from story_generator.messages import Messages


def test_message_creation():
    messages = Messages()
    assert messages.messages == []

def test_add_user_message():
    messages = Messages()
    messages.add_user_message("Hello")
    assert messages.messages == [{
        "role": "user",
        "content": "Hello",
    }]

def test_add_assistant_message():
    messages = Messages()
    messages.add_assistant_message("Hello")
    assert messages.messages == [{
        "role": "assistant",
        "content": "Hello",
    }]

def test_add_system_message():
    messages = Messages()
    messages.add_system_message("Hello")
    assert messages.messages == [{
        "role": "system",
        "content": "Hello",
    }]

def test_add_multiple_messages():
    messages = Messages()
    messages.add_user_message("Hello User")
    messages.add_assistant_message("Hello Assistant")
    messages.add_system_message("Hello System")
    assert messages.messages == [{
        "role": "user",
        "content": "Hello User",
    }, {
        "role": "assistant",
        "content": "Hello Assistant",
    }, {
        "role": "system",
        "content": "Hello System",
    }]

def test_remove_last_message():
    messages = Messages()
    messages.add_user_message("First Message")
    messages.add_user_message("Second Message")
    assert len(messages.messages) == 2

    messages.remove_last_message()
    assert len(messages.messages) == 1
    messages.remove_last_message()
    assert len(messages.messages) == 0
    messages.remove_last_message()
    assert len(messages.messages) == 0


def test_write_to_file():
    messages = Messages()
    messages.add_user_message("Test Message")
    mocked_file = mock_open()
    with patch('builtins.open', mocked_file):
        messages.write_to_file("test.json")

    mocked_file.assert_called_once_with("test.json", "w")
    expected_json = json.dumps({"messages": [{"role": "user", "content": "Test Message"}]}, indent=2)
    mocked_file().write.assert_called_once_with(expected_json)


@unittest.mock.patch('builtins.open', create=True)
@unittest.mock.patch('story_generator.pages.get_path_to_summaries')
@unittest.mock.patch('story_generator.pages.get_chapters_from_page')
def test_add_summary_so_far(mock_get_chapters_from_page, mock_get_path, mock_open):
    mock_get_path.return_value = "mock/path"
    mock_get_chapters_from_page.side_effect = [['chapter 1', 'chapter 2'], ['chapter 3', 'chapter 4']]
    mock_open.return_value.__enter__.return_value.read.return_value = "mock content"

    messages = Messages()
    messages.add_summary_so_far('Test Example', ['page1.txt', 'page2.txt'])

    assert len(messages.messages) == 1
