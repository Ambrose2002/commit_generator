"""CLI entrypoint for generating and applying Conventional Commits.

Run this script from a git repo path to generate a commit message from staged
diffs using the configured AI model, then optionally apply the commit.
"""

from git_cli import get_diff, commit_changes
from commits import generate_commit
import sys

MODEL = "sonar-pro"


def run(file_path: str) -> str:
    """
    Execute the commit message generation workflow.

    Retrieves diffs from the current directory, generates an appropriate
    commit message using the configured model, and returns the result.

    Returns:
        str: The generated commit message if successful, "No diffs found" if
             no diffs are available, or an empty string if message generation fails.
    """
    success, diffs = get_diff(file_path)

    if not success or not diffs:
        return "No diffs found"

    success, message = generate_commit(diffs, model_name=MODEL)

    if success:
        return message
    return ""


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python app.py <directory>")
    else:
        file_path = sys.argv[1]
        message = run(file_path)
        
        if len(message):
            print(message)
            response = input("Do you want to commit with this message? y/n: ")
            if response.lower() == "y":
                print("Commiting changes...")
                success, msg = commit_changes(file_path, message)
                if success:
                    print("Changes commited")
                else:
                    print("Error: commit failed")
            else:
                print("Commit ignored")
        else:
            print("Error: commit message generated")
