from story_generator.grok import get_client, ask_grok
from story_generator.instructions import get_expanded_story_instructions, get_html_format_instructions
from story_generator.messages import Messages
from story_generator.pages import (
    get_chapters_from_page,
    write_page_to_file,
    get_story_page_from_summary_page,
    get_html,
    get_message_page_from_summary_page,
    get_list_of_remaining_summary_pages,
)

title = 'Example'
client = get_client()
for page in get_list_of_remaining_summary_pages(title):
    print(f"Processing page: {page}")
    messages = Messages()
    messages.add_system_message(get_expanded_story_instructions())
    messages.add_system_message(get_html_format_instructions())
    messages.add_summary_so_far(title, page)

    page_text = []
    for chapter in get_chapters_from_page(title, page):
        messages.add_user_message(chapter)
        story = ask_grok(client, messages)
        messages.add_assistant_message(story)
        page_text.append(story)

    story_page = get_story_page_from_summary_page(page)
    write_page_to_file(title, story_page, get_html(title, '\n'.join(page_text)))
    messages.write_to_file(get_message_page_from_summary_page(f'{title}/{page}'))

