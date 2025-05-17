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
