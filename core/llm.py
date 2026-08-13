"""
ARC LLM interface.

Handles communication with the local Llama model
running through Ollama.
"""

from ollama import chat


MODEL_NAME = "llama3.2:3b"


def ask_llm(messages: list[dict]) -> str:
    """
    Send conversation messages to the local Llama model
    and return the generated response.
    """

    response = chat(
        model=MODEL_NAME,
        messages=messages,
    )

    return response["message"]["content"]