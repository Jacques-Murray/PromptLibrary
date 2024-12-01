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

class LLMClient:
    """Client for interacting with different LLM providers."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
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
    
    # Use default OpenAI config if none provided
    if config is None:
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4",
            temperature=0.7
        )
    
    # Use template from PROMPT_GENERATOR if none provided
    template = template or PROMPT_GENERATOR.template
    if format_args:
        template = template.format(**format_args)
    
    client = LLMClient(config)
    return client.generate(
        system_prompt=template,
        user_prompt=f"Task, Goal, or Current Prompt:\n{task_or_prompt}"
    )
