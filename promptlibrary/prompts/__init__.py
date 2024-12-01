"""
Collection of pre-defined prompts organized by category.
"""

from .coding import CODE_REVIEW_PROMPT
from .meta import META_PROMPT, generate_prompt
from .philosophical import AI_ETHICS_EXPLORATION
from .system import PROMPT_GENERATOR

__all__ = [
    'CODE_REVIEW_PROMPT',
    'META_PROMPT',
    'generate_prompt',
    'AI_ETHICS_EXPLORATION',
    'PROMPT_GENERATOR'
]
