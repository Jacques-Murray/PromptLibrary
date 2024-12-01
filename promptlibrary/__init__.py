"""
PromptLibrary - A Python package for managing and organizing prompts.
"""

from .llm import (
    LLMProvider, LLMConfig, LLMClient,
    create_prompt, edit_prompt, generate_prompt
)

__version__ = "0.1.0"

__all__ = [
    'LLMProvider',
    'LLMConfig',
    'LLMClient',
    'create_prompt',
    'edit_prompt',
    'generate_prompt'
]
