import inquirer

from story_generator.pages import get_summary_directories


def select_title() -> str:
    questions = [
        inquirer.List('directory',
          message="Select story you want to generate:",
          choices=sorted(get_summary_directories()),
          carousel=True  # Allows wrapping around the list
        )
    ]

    answers = inquirer.prompt(questions)
    return answers['directory']


# Example usage:
if __name__ == "__main__":
    selected = select_title()
    print(f"\nYou selected: {selected}")
