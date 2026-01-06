from perplexity import Perplexity, BadRequestError, RateLimitError, APIStatusError


def generate_prompt(diffs: str) -> str:
    """Generate a prompt template for creating a Conventional Commits message from git diffs.

    This function constructs a detailed prompt instruction that guides an AI model
    to analyze git diffs and produce a properly formatted commit message following
    the Conventional Commits specification.

    Args:
        diffs (str): The git diff content to be analyzed for generating the commit message.

    Returns:
        str: A formatted prompt template containing instructions for generating a commit message
             with the following specifications:
    """
    template = f"""You are a senior software engineer. Write a single commit message following Conventional Commits, based only on the provided git diff.

        Input:
        - diffs: {diffs}

        Output format (return only the commit text):
        type: subject

        body (wrapped at ~72 chars)

        BREAKING CHANGE: <description>  # include only if needed

        Rules:
        - Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert.
        - Subject: imperative mood, <=72 chars, no trailing period.
        - No scope and no ticket footers.
        - Summarize what and why from the diff; do not invent changes.
        - Return only the commit message text.
    """

    return template


def generate_commit(diffs: str, model_name: str = "sonar-pro") -> tuple[bool, str]:
    """
    Generate a commit message using the Perplexity API based on provided diffs.
    
    Args:
        diffs (str): The diff content to generate a commit message for.
        model_name (str, optional): The model to use for generation. Defaults to "sonar-pro".
    
    Returns:
        str: The generated commit message on success.
        tuple: A tuple of (False, error_message) if a BadRequestError, RateLimitError, or APIStatusError occurs.
    
    Raises:
        Handles BadRequestError, RateLimitError, and APIStatusError internally and returns False with error message.
    """

    # Initialize the client (uses PERPLEXITY_API_KEY environment variable)
    client = Perplexity()

    template = generate_prompt(diffs)

    try:
        # Make the API call
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": template}],
            stream=False,
        )
        content = completion.choices[0].message.content
        if isinstance(content, str):
            return True, content
        else:
            return True, str(content) if content is not None else ""

    except BadRequestError as e:
        return False, str(e)

    except RateLimitError as e:
        return False, str(e)

    except APIStatusError as e:
        return False, str(e)

