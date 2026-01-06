from perplexity import Perplexity, BadRequestError, RateLimitError, APIStatusError
import re

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
        - Do NOT use Markdown, code fences, backticks, or quotes around the message.

    """

    return template

def _sanitize_commit_text(text: str) -> str:
    """Remove surrounding Markdown/code fences and quotes if present."""
    s = text.strip()

    # Triple backtick block with optional language
    m = re.match(r"^```[a-zA-Z0-9+\-_.]*\n([\s\S]*?)\n```$", s)
    if m:
        return m.group(1).strip()

    # Inline or generic fenced block on one line
    m = re.match(r"^```([\s\S]*?)```$", s)
    if m:
        return m.group(1).strip()

    # Any surrounding backticks (1-3)
    m = re.match(r"^`{1,3}([\s\S]*?)`{1,3}$", s)
    if m:
        return m.group(1).strip()

    # Surrounding single or double quotes
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1].strip()

    return s

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
        text = content if isinstance(content, str) else (str(content) if content is not None else "")
        return True, _sanitize_commit_text(text)

    except BadRequestError as e:
        return False, str(e)

    except RateLimitError as e:
        return False, str(e)

    except APIStatusError as e:
        return False, str(e)
