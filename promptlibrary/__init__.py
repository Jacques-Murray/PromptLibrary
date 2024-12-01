"""
A Python package for managing and enhancing prompts for language models.
"""

from .llm import (
    generate_prompt,
    generate_audio_prompt,
    create_prompt,
    create_audio_prompt,
    edit_prompt,
    edit_audio_prompt,
    generate_schema,
    LLMConfig,
    LLMProvider,
    LLMClient
)

from .schema import (
    Schema,
    SchemaProperty,
    FUNCTION_META_SCHEMA
)

from .prompts.system import FUNCTION_SCHEMA_GENERATOR

__version__ = "0.1.0"

__all__ = [
    'Schema',
    'SchemaProperty',
    'FUNCTION_META_SCHEMA',
    'FUNCTION_SCHEMA_GENERATOR',
    'generate_schema',
    'edit_audio_prompt'
]
