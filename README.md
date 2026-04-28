A simple way to think about it:

uv sync --dev = put the tool in your venv
pre-commit install = connect the tool to Git commits
pre-commit run --all-files = use the tool right now
So for your case, because git commit did not trigger anything, the missing step was:

uv run pre-commit install
Then optionally test it with:

uv run pre-commit run --all-files
