# story_generator
Use the power of AI to create stories

## Usage
This script will iterate over pages in a directory placed inside the `summaries` directory. Each page should contain a few paragraphs separated by one or more return characters "\n" (See `summaries/Example`). Each paragraph will be given, one-by-one, to the LLM to be expanded. The shorter the paragraph, the more creative the LLM will get. So experiment with the length of each paragraph. There can't be any carriage returns within a paragraph, so make sure Soft-wrap is checked on if writing in an IDE. The number of paragraphs per page is up to you.

Each summary page will be expanded into a story html page that is written to the `stories` directory. The name of the directory that contains your summaries, will be the name of the directory that contains your stories.


## Setup
This script uses Grok as the LLM. You will need to set up an X.ai account at https://accounts.x.ai/sign-up. Once signed in, you will need to go to the API console, add some funds to your account, and create an API key. This key should look like xai-blahblahblah...

Now inside the `local` directory, create a file called .env with the following contents:
```dotenv
XAI_API_KEY=YOUR_XAI_API_KEY_GOES_HERE
```

## Running the script
To run the script, type `python example.py` in the command line. For now the title (directory containing the summaries) must be hard coded in the example.py file.
