from story_generator.instructions import get_html_format_instructions, get_expanded_story_instructions, get_current_scene, get_next_scene


def test_get_html_format_instructions():
    result = get_html_format_instructions()
    assert isinstance(result, str)

def test_get_expanded_story_instructions():
    result = get_expanded_story_instructions()
    assert isinstance(result, str)

def test_get_current_scene():
    result = get_current_scene()
    assert isinstance(result, str)

def test_get_next_scene():
    result = get_next_scene()
    assert isinstance(result, str)
