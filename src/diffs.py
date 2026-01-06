import subprocess


def get_diff(file_path: str) -> tuple[bool, str]:
    """
    Retrieve the staged git diff for a repository.
    
    Args:
        file_path (str): The path to the git repository directory.
    
    Returns:
        tuple[bool, str]: A tuple containing:
            - bool: True if the git diff command succeeded, False otherwise.
            - str: The staged diff output if successful, or an error message if failed.
    
    Raises:
        No exceptions are raised. Errors are caught and returned as a tuple.
    """

    try:
        result = subprocess.run(
            ["git", "diff", "--staged"],
            cwd=file_path,
            capture_output=True,
            text=True,
        )

        if result.stderr:
            return False, result.stderr

        return True, result.stdout

    except Exception as e:
        return False, str(e)

