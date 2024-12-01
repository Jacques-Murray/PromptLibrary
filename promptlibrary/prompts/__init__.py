"""
Collection of pre-defined prompts organized by category.
"""

from .coding import CODE_REVIEW_PROMPT
from .meta import META_PROMPT, generate_prompt

__all__ = [
    'CODE_REVIEW_PROMPT',
    'META_PROMPT',
    'generate_prompt'
]
