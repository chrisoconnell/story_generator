import unittest.mock
from story_generator.instructions import get_html_format_instructions, get_expanded_story_instructions, get_current_scene, get_next_scene, \
    _get_local_overrides_module, _get_local_defaults, get_continue_story


def test_get_html_format_instructions():
    result = get_html_format_instructions()
    assert isinstance(result, str)

def test_get_expanded_story_instructions():
    result = get_expanded_story_instructions()
    print(result)
    assert isinstance(result, str)

def test_get_current_scene():
    result = get_current_scene('Example Scene')
    assert isinstance(result, str)

def test_get_next_scene():
    result = get_next_scene('Example Scene')
    assert isinstance(result, str)

def test_get_continue_story():
    result = get_continue_story(['chapter 1', 'chapter 2'])
    assert isinstance(result, str)


@unittest.mock.patch('story_generator.instructions._get_local_overrides_module')
def test_get_local_defaults_with_no_overrides(mock_get_local):
    mock_get_local.return_value = False
    result = _get_local_defaults()
    mock_get_local.assert_called_once()
    assert result == {}

@unittest.mock.patch('story_generator.instructions._get_local_overrides_module')
def test_get_local_defaults_with_overrides(mock_get_local):
    local_instructions = {'expanded_story_instructions': "local instructions",}
    mock_get_local.return_value.local_overrides = local_instructions
    result = _get_local_defaults()
    assert result == local_instructions


@unittest.mock.patch('importlib.util.spec_from_file_location')
@unittest.mock.patch('importlib.util.module_from_spec')
@unittest.mock.patch('os.path.exists')
def test_get_local_overrides_module_success(mock_exists, mock_module_from_spec, mock_spec_from_file):
    mock_exists.return_value = True
    mock_spec = unittest.mock.Mock()
    mock_spec_from_file.return_value = mock_spec
    mock_module = unittest.mock.Mock()
    mock_module_from_spec.return_value = mock_module

    result = _get_local_overrides_module()

    assert result == mock_module
    mock_exists.assert_called_once()
    mock_spec_from_file.assert_called_once()
    mock_module_from_spec.assert_called_once_with(mock_spec)
    mock_spec.loader.exec_module.assert_called_once_with(mock_module)


def test_get_local_overrides_module_no_file(mock_exists):
    mock_exists.return_value = False

    result = _get_local_overrides_module()

    assert result is False
    mock_exists.assert_called_once()
