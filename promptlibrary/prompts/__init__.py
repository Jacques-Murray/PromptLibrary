"""
Collection of pre-defined prompts organized by category.
"""

from .coding import CODE_REVIEW_PROMPT
from .meta import META_PROMPT, generate_prompt
from .philosophical import AI_ETHICS_EXPLORATION

__all__ = [
    'CODE_REVIEW_PROMPT',
    'META_PROMPT',
    'generate_prompt',
    'AI_ETHICS_EXPLORATION'
]
