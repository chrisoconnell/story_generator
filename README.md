# story_generator
Use the power of AI to create stories

## Usage
This script will iterate over pages in a directory placed inside the `summaries` directory. Each page should contain a few paragraphs separated by one or more return characters "\n" (See `summaries/Example`). Each paragraph will be given, one-by-one, to the LLM to be expanded. The shorter the paragraph, the more creative the LLM will get. So experiment with the length of each paragraph. There can't be any carriage returns within a paragraph, so make sure Soft-wrap is checked on if writing in an IDE. The number of paragraphs per page is up to you.

Each summary page will be expanded into a story html page that is written to the `stories` directory. The name of the directory that contains your summaries, will be the name of the directory that contains your stories.

You can add to the story at any time by adding more pages to the summaries directory and re-running the script. The script will only expand the pages that have not been expanded yet.


## Setup
This script uses Grok as the LLM. You will need to set up an X.ai account at https://accounts.x.ai/sign-up. Once signed in, you will need to go to the API console, add some funds to your account, and create an API key. This key should look like xai-blahblahblah...

Now inside the `local` directory, create a file called .env with the following contents:
```dotenv
XAI_API_KEY=YOUR_XAI_API_KEY_GOES_HERE
```

### Optional
If you want to override the instructions given to the LLM, you can create a file called `instructions.py` in the `local` directory. This file should contain a dictionary called `local_overrides` with the instructions you want to override.

For example:
```python
local_overrides = {
    'expanded_story_instructions': "You are Andy, a popular sci-fi writer that loves to write stories that have unexpected plot twists...",
}
```
It works best if you copy/paste the `_defaults` dictionary from the story_generator/instructions.py file and just modify the instructions you want to override. Do not include instructions that you want to keep the default.

## Running the script
To run the script, type `python example.py` in the command line. You will be prompted to select the name of the directory that contains your summaries.
