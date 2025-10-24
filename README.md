
# Git Agent

A small interactive Git assistant built with Python and LangChain. This project provides a command-line agent that exposes common Git operations (init, status, add, commit, push, pull, clone, diff, etc.) as tools callable by a language model. The agent runs locally and streams responses while using the provided tools to run Git and file operations.

## Features

- Interactive command-line agent that accepts prompts and executes git/file tools.
- Tools implemented: git init/status/add/commit/log/branch/checkout/merge/push/pull/clone/diff/reset and file read/write/tree.
- Middleware error handling to return helpful tool error messages.

## Requirements

- Python 3.8+
- See `requirements.txt` for runtime dependencies.

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Configuration (.env)

Create a `.env` file in the repository root (next to `requirements.txt` and this README). The code expects a few environment variables used by the language model client. Example `.env` content:

```bash
DEFAULT_MODEL=your-model-name
BASE_URL=https://api.your-llm-provider.com
# If your provider uses an API key, set it here too (example variable, provider-specific name may vary):
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

Adjust variables according to your model/provider setup. `src/main.py` references `DEFAULT_MODEL` and `BASE_URL`. Your provider may require additional environment variables.

## How to run

1. Install dependencies (see above).
2. Create `.env` with the necessary model/credentials.
3. Run the agent:

```bash
python3 src/main.py
```

When it starts you'll see a prompt. Type natural language commands describing git tasks (for example: "Show git status in /path/to/repo", "Create a new branch named feature/x", "Add and commit file README.md with message 'update'", etc.). Type `exit` to quit.

## Notes and safety

- The agent executes Git commands on the paths you supply. Use caution and test on throwaway repositories if you are experimenting.
- The code uses a language model to decide which tools to call — always review the agent output and results before applying important changes to production repositories.

## Contributing

Contributions are welcome. If you add tools or change behavior, please update these READMEs and add tests where appropriate.
