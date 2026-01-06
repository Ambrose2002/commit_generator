from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def generate_promt(diffs: str):

    template = """You are a senior software engineer. Write a single commit message following Conventional Commits, based only on the provided git diff.

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

    return ChatPromptTemplate.from_template(template)

def generate_commit(diffs: str, model_name: str, f: str = ""):
    
    model = OllamaLLM(model = model_name, format=f)  # type: ignore
    
    chain = generate_promt(diffs) | model
    
    return chain.invoke

print(generate_commit("Hello", "llama3.1"))
