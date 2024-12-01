"""
A Python package for managing and enhancing prompts for language models.
"""

from .llm import (
    generate_prompt,
    generate_audio_prompt,
    create_prompt,
    create_audio_prompt,
    edit_prompt,
    LLMConfig,
    LLMProvider,
    LLMClient
)

__version__ = "0.1.0"

__all__ = [
    'generate_prompt',
    'generate_audio_prompt',
    'create_prompt',
    'create_audio_prompt',
    'edit_prompt',
    'LLMConfig',
    'LLMProvider',
    'LLMClient'
]
