# commit_generator

CLI helper that drafts Conventional Commits from your staged diffs using the Perplexity API, then optionally commits them for you.

## Install
- Python 3.10+ required.
- From the repo root, install with console entrypoint: `pip install -e .`
- Set your API key: `export PERPLEXITY_API_KEY=<key>`

## Usage
1. Stage changes in the target repo: `git add ...`
2. Run the CLI from anywhere, pointing at that repo path: `cgm <path-to-repo>`
3. Review the generated Conventional Commit message; enter `y` to commit, anything else to skip.

## Behavior
- Uses model `sonar-pro` to generate a single Conventional Commit message (type + subject, optional body/breaking change).
- If no staged diffs are found, it reports "No diffs found" and exits.
- Commits are executed in the directory you pass as the argument.

## Troubleshooting
- If you see API errors, verify `PERPLEXITY_API_KEY` is set and your network allows outbound requests.
- If git commands fail, confirm the path you pass points to a git repository with staged changes.
