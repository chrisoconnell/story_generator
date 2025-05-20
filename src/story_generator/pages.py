import os


def get_path_to_summaries(title: str = None) -> str:
    path = f"summaries/{title}" if title else "summaries"
    return _get_absolute_path(path)

def get_path_to_stories(title: str = None) -> str:
    path = f"stories/{title}" if title else "stories"
    return _get_absolute_path(path)

def get_path_to_local(filename: str) -> str:
    return _get_absolute_path(f"local/{filename}")

def get_summary_pages(title: str) -> list:
    path = get_path_to_summaries(title)
    return sorted(os.listdir(path))

def get_summary_directories() -> list:
    path = get_path_to_summaries()
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]


def get_story_page_from_summary_page(page: str):
    return page.replace(".txt", ".htm")

def get_message_page_from_summary_page(page: str):
    return page.replace(".txt", "_messages.json")

def get_list_of_summary_pages(title: str) -> list:
    return os.listdir(get_path_to_summaries(title))

def _has_corresponding_story_page(title: str, page: str) -> bool:
    story_page = get_story_page_from_summary_page(page)
    return os.path.exists(get_path_to_stories(f"{title}/{story_page}"))

# Get a list of summary pages that don't have a corresponding story page.
def get_list_of_remaining_summary_pages(title: str) -> list:
    pages = get_list_of_summary_pages(title)
    return sorted(filter(lambda p: not _has_corresponding_story_page(title, p), pages))

def get_pages_before_current_page(title: str, page: str) -> list:
    pages = get_list_of_summary_pages(title)
    return pages[:pages.index(page)]


def get_chapters_from_page(title: str, page) -> list:
    with open(get_path_to_summaries(f"{title}/{page}"), "r") as f:
        return _filter_and_trim(f.read().split("\n"))

def write_page_to_file(title: str, page: str, content: str):
    _create_dir(get_path_to_stories(title))
    with open(get_path_to_stories(f"{title}/{page}"), "w") as f:
        f.write(content)

def get_html(title: str, story: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>{title}</title>
        <style>
            body {{
                width: 960px; margin: 0 auto; font-size: larger;        
            }}
        </style>
    </head>
    <body>
        {story}
    </body>
</html>
    """.strip()


def _get_absolute_path(path: str) -> str:
    paths = path.split('/')
    fullpath = os.path.join(os.path.dirname(__file__), "..", "..", *paths)
    return os.path.abspath(str(fullpath))

def _filter_and_trim(chapters: list) -> list:
    return [chapter.strip(' ') for chapter in chapters if chapter]

def _create_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)