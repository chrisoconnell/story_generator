import os
import importlib.util

from story_generator.pages import get_path_to_local

_defaults = {
    'html_format_instructions': "You will provide the novel in HTML format. This will not be a complete HTML page, rather it is meant to be pasted into the body of an HTML page so will not include styles or header tags. You will use html entities like &ldquo; and &rdquo inplace of special characters like “ and ”.  Do not add titles/chapters/etc. to the story, that is handled later.",

    'expanded_story_instructions': "You are Steven, a popular novel writer that loves to write stories that have good character development, plot, and story. You are also a master at writing in the first person, very good at getting the reader to feel the emotions of the protagonist, being able to live vicariously through them. You will be building a story, one scene at a time. You will be given a short description of the scene, from which you will write out a fully formed scene, writing as much as you can about that scene. You will not continue the story from where the scene leaves off, nor write the precursor to the scene. You are just making this scene as detailed as possible. All names, locations, plot points, character development/description, and such should remain the same from what you are given. At the start of each new scene you write, continue right where you left off previously.",

    'current_scene': "Current scene: ",

    'next_scene': "Next scene: ",

    'continue_story': "Here is a summary of the story so far. Don't expand on this, its just here for your reference. You will be picking up where this summary leaves off:",
}

def _get_local_overrides_module():
    local_instructions = get_path_to_local('instructions.py')
    if not os.path.exists(local_instructions):
        return False

    spec = importlib.util.spec_from_file_location('local', local_instructions)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, 'local_overrides'):
        return False

    return module


def _get_local_defaults() -> dict:
    module = _get_local_overrides_module()
    if not module:
        return {}

    return module.local_overrides


_merged_defaults = {**_defaults, **_get_local_defaults()}


def get_html_format_instructions() -> str:
    return _merged_defaults['html_format_instructions']


def get_expanded_story_instructions() -> str:
    return _merged_defaults['expanded_story_instructions']


def get_current_scene(scene: str) -> str:
    return _merged_defaults['current_scene'] + scene


def get_next_scene(scene: str) -> str:
    return _merged_defaults['next_scene'] + scene


def get_continue_story(chapters: list[str]) -> str:
    return _merged_defaults['continue_story'] + '\n'.join(chapters)
