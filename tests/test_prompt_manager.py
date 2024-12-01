"""
Tests for the PromptManager class.
"""

import pytest
from promptlibrary.prompt_manager import PromptManager
from promptlibrary.models import Prompt, PromptCategory

@pytest.fixture
def sample_prompt():
    return Prompt(
        name="test_prompt",
        category=PromptCategory.CODING,
        description="A test prompt",
        template="This is a test prompt with {variable}",
        tags=["test", "example"],
        model_compatibility=["gpt-3.5-turbo"],
        parameters={"variable": "A test variable"}
    )

def test_prompt_manager_initialization():
    """Test that PromptManager initializes correctly."""
    manager = PromptManager()
    assert isinstance(manager.prompts, dict)
    assert len(manager.prompts) == 0

def test_add_and_get_prompt(sample_prompt):
    """Test adding and retrieving prompts."""
    manager = PromptManager()
    manager.add_prompt(sample_prompt)
    
    retrieved = manager.get_prompt("test_prompt")
    assert retrieved == sample_prompt
    
def test_get_prompts_by_category(sample_prompt):
    """Test filtering prompts by category."""
    manager = PromptManager()
    manager.add_prompt(sample_prompt)
    
    coding_prompts = manager.get_prompts_by_category(PromptCategory.CODING)
    assert len(coding_prompts) == 1
    assert coding_prompts[0] == sample_prompt
    
    writing_prompts = manager.get_prompts_by_category(PromptCategory.WRITING)
    assert len(writing_prompts) == 0

def test_get_prompts_by_tag(sample_prompt):
    """Test filtering prompts by tag."""
    manager = PromptManager()
    manager.add_prompt(sample_prompt)
    
    test_prompts = manager.get_prompts_by_tag("test")
    assert len(test_prompts) == 1
    assert test_prompts[0] == sample_prompt
    
    nonexistent_prompts = manager.get_prompts_by_tag("nonexistent")
    assert len(nonexistent_prompts) == 0
