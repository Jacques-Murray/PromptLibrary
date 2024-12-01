"""Module for handling LLM interactions."""
from typing import Optional, Union, List, Dict
from dataclasses import dataclass
import os
from enum import Enum

class LLMProvider(Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"

@dataclass
class LLMConfig:
    """Configuration for LLM client."""
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None

    @classmethod
    def default_openai(cls) -> 'LLMConfig':
        """Create a default OpenAI configuration using GPT-4."""
        return cls(
            provider=LLMProvider.OPENAI,
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    @classmethod
    def default_ollama(cls) -> 'LLMConfig':
        """Create a default Ollama configuration using llama3.2."""
        return cls(
            provider=LLMProvider.OLLAMA,
            model="llama3.2"
        )

class LLMClient:
    """Client for interacting with different LLM providers."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """Initialize the client with optional configuration.
        
        Args:
            config: LLM configuration. If None, uses default OpenAI config.
        """
        self.config = config or LLMConfig.default_openai()
        self._client = None
        self._setup_client()
    
    def _setup_client(self):
        """Initialize the appropriate LLM client based on provider."""
        if self.config.provider == LLMProvider.OPENAI:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.config.api_key or os.getenv("OPENAI_API_KEY"),
                    base_url=self.config.base_url
                )
            except ImportError:
                raise ImportError("OpenAI package not found. Install with: pip install openai")
        elif self.config.provider == LLMProvider.OLLAMA:
            try:
                import ollama
                self._client = ollama
            except ImportError:
                raise ImportError("Ollama package not found. Install with: pip install ollama")
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> str:
        """Generate completion using the configured LLM.
        
        Args:
            system_prompt: The system prompt to guide the model
            user_prompt: The user's input prompt
            **kwargs: Additional provider-specific parameters
            
        Returns:
            str: The generated completion text
            
        Raises:
            RuntimeError: If the LLM client fails or returns an error
        """
        try:
            if self.config.provider == LLMProvider.OPENAI:
                response = self._client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                    **kwargs
                )
                return response.choices[0].message.content
                
            elif self.config.provider == LLMProvider.OLLAMA:
                response = self._client.chat(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    **kwargs
                )
                return response['message']['content']
                
        except Exception as e:
            raise RuntimeError(f"Error generating completion: {str(e)}")

def create_prompt(
    task_or_prompt: str,
    config: Optional[LLMConfig] = None,
    template: str = None,
    format_args: Dict = None
) -> str:
    """Generate a prompt using the configured LLM.
    
    Args:
        task_or_prompt: The task description or existing prompt to improve
        config: LLM configuration. If None, uses default OpenAI config
        template: Optional custom template. If None, uses default META_PROMPT
        format_args: Optional arguments to format the template
        
    Returns:
        str: The generated prompt
        
    Raises:
        RuntimeError: If prompt generation fails
    """
    from .prompts.system import PROMPT_GENERATOR
    
    # Use template from PROMPT_GENERATOR if none provided
    template = template or PROMPT_GENERATOR.template
    if format_args:
        template = template.format(**format_args)
    
    client = LLMClient(config)
    return client.generate(
        system_prompt=template,
        user_prompt=f"Task, Goal, or Current Prompt:\n{task_or_prompt}"
    )

def edit_prompt(
    current_prompt: str,
    change_description: str,
    config: Optional[LLMConfig] = None,
    template: str = None,
    format_args: Dict = None
) -> str:
    """Edit an existing prompt based on a change description.
    
    Args:
        current_prompt: The existing prompt to modify
        change_description: Description of the changes to make
        config: LLM configuration. If None, uses default OpenAI config
        template: Optional custom template. If None, uses default PROMPT_EDITOR
        format_args: Optional arguments to format the template
        
    Returns:
        str: The edited prompt
        
    Raises:
        RuntimeError: If prompt editing fails
    """
    from .prompts.system import PROMPT_EDITOR
    
    # Use template from PROMPT_EDITOR if none provided
    template = template or PROMPT_EDITOR.template
    if format_args:
        template = template.format(**format_args)
    
    client = LLMClient(config)
    return client.generate(
        system_prompt=template,
        user_prompt=f"""Current Prompt:
{current_prompt}

Change Description:
{change_description}"""
    )

# Simple function matching the example code's interface
def generate_prompt(task_or_prompt: str, model: str = "gpt-4o") -> str:
    """Simple interface for generating prompts using OpenAI.
    
    This matches the interface of the example code while using our robust implementation.
    
    Args:
        task_or_prompt: The task description or existing prompt to improve
        model: The OpenAI model to use (default: "gpt-4o")
        
    Returns:
        str: The generated prompt
    """
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model=model
    )
    return create_prompt(task_or_prompt, config=config)
