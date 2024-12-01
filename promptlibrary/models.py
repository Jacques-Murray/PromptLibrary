from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class PromptCategory(Enum):
    CODING = "coding"
    WRITING = "writing"
    ANALYSIS = "analysis"
    CHAT = "chat"
    SYSTEM = "system"
    GENERAL = "general"
    PHILOSOPHICAL = "philosophical"

@dataclass
class Prompt:
    """Represents a single prompt template with its metadata."""
    template: str
    category: PromptCategory
    name: str
    description: str
    tags: List[str] = field(default_factory=list)
    model_compatibility: List[str] = field(default_factory=list)
    parameters: Dict[str, str] = field(default_factory=dict)
    version: str = "1.0"
    
    def format(self, **kwargs) -> str:
        """Format the prompt template with the given parameters."""
        return self.template.format(**kwargs)
