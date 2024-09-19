EigenGen
========

EigenGen is a CLI Large Language Model frontend. It is geared towards working with code,
and supports a code review flow where you request changes and review patches suggested
by the tool similar to classic email based patch review.

EigenGen works with 
  - Anthropic claude-3-5-sonnet
  - OpenAI GPT4o
  - llama3.1:70b via Groq

## Features

  - Basic prompt/answer flow with -p "Type your prompt here"
  - Diff output mode with -d that prints out the changes to files as a diff
  - Code Review flow with -r that gives you the option to continue discussing the changes with the LLM
    by typing your comments in-line with '> ' quoted diff. This is a bit like software development used to be before Pull Requests.
  - Add 'git ls-files' files to context automatically with -g, filtered by .eigengen_ignore.


## Installation
```
pip install eigengen
```

You must export your API key using:
```
export ANTHROPIC_API_KEY=<your-api-key>
or
export OPENAI_API_KEY=<your-api-key>
or
export GROQ_API_KEY=<your-api-key>
```

## Development

Please install in edit mode like this:
```
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

For testing install pytest.


## Example Usage

```
# start a new code review flow to develop a TODO-list web app
eigengen -r -g -p "Please implement a TODO-list web app using react + javascript, thank you. Provide the full project directory structure, please. It should allow adding, editing and deleting entries."

# pipe file content in through stdin
cat setup.py | eigengen -f - -p "Please review the given source file, thank you!"

# pipe a git diff output and write a review for it
git diff origin/main^^..HEAD | eigengen -f - -p "Please write a code review for the given diff, thank you!
```

By default eigengen uses claude-3-5-sonnet. In order to use OpenAI GPT4o model, please give --model, -m argument
like this:
```
eigengen -m gpt4 -p "your prompt content"
```

You may wish to create a shell alias to avoid having to type it in all the time:
```.bashrc
alias eigengen='eigengen -m gpt4'
```


TODO:
  - Figure out why Mistral's models just hate our system prompts.
  - Add some kind of directory indexing machinery to lessen the need to list files manually.

