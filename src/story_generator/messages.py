import json

from story_generator.instructions import get_continue_story
from story_generator.pages import get_path_to_stories, get_chapters_from_page, get_pages_before_current_page


class Messages:
    def __init__(self):
        self.messages = []

    def add_user_message(self, message: str) -> None:
        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, message: str) -> None:
        self.messages.append({"role": "assistant", "content": message})

    def add_system_message(self, message: str) -> None:
        self.messages.append({"role": "system", "content": message})

    def remove_last_message(self) -> None:
        if len(self.messages) > 0:
            self.messages.pop()

    def add_summary_so_far(self, title: str, page: str) -> None:
        pages = get_pages_before_current_page(title, page)
        if len(pages) == 0:
            return

        chapters = []
        for page in pages:
            chapters.extend(get_chapters_from_page(title, page))

        self.add_user_message(get_continue_story(chapters))

    def write_to_file(self, filename: str) -> None:
        file_path = get_path_to_stories(filename)
        with open(file_path, "w") as file:
            file.write(json.dumps({"messages": self.messages}, indent=2))

