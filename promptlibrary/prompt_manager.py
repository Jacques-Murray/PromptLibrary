"""
Core module for managing prompts.
"""
from typing import Dict, List, Optional
from .models import Prompt, PromptCategory

class PromptManager:
    """A class to manage and organize prompts."""
    
    def __init__(self):
        """Initialize the PromptManager."""
        self.prompts: Dict[str, Prompt] = {}
        
    def add_prompt(self, prompt: Prompt) -> None:
        """Add a prompt to the manager."""
        self.prompts[prompt.name] = prompt
    
    def get_prompt(self, name: str) -> Optional[Prompt]:
        """Get a prompt by name."""
        return self.prompts.get(name)
    
    def get_prompts_by_category(self, category: PromptCategory) -> List[Prompt]:
        """Get all prompts in a specific category."""
        return [p for p in self.prompts.values() if p.category == category]
    
    def get_prompts_by_tag(self, tag: str) -> List[Prompt]:
        """Get all prompts with a specific tag."""
        return [p for p in self.prompts.values() if tag in p.tags]
