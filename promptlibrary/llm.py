"""Module for handling LLM interactions."""
from typing import Optional, Union, List, Dict, Any
from dataclasses import dataclass
import os
from enum import Enum
from openai import OpenAI
import json

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
    """Client for interacting with LLMs."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        if config.provider == LLMProvider.OPENAI:
            self.client = OpenAI(api_key=config.api_key)
        elif config.provider == LLMProvider.OLLAMA:
            import ollama
            self.client = ollama
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")

    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional arguments to pass to the LLM
            
        Returns:
            str: The generated response
        """
        if self.config.provider == LLMProvider.OPENAI:
            completion = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                **kwargs
            )
            return completion.choices[0].message.content
        
        elif self.config.provider == LLMProvider.OLLAMA:
            response = self.client.chat(
                model=self.config.model,
                messages=messages,
                **kwargs
            )
            return response['message']['content']

def create_prompt(task_or_prompt: str, config: Optional[LLMConfig] = None) -> str:
    """Create a new prompt based on a task description.
    
    Args:
        task_or_prompt: Description of the task or existing prompt to improve
        config: Optional LLM configuration. If not provided, uses default OpenAI config
        
    Returns:
        str: The generated prompt
    """
    from .prompts.system import PROMPT_GENERATOR
    
    if config is None:
        config = LLMConfig.default_openai()
    
    client = LLMClient(config)
    return client.generate([
        {
            "role": "system",
            "content": PROMPT_GENERATOR.content,
        },
        {
            "role": "user",
            "content": "Task, Goal, or Current Prompt:\n" + task_or_prompt,
        },
    ])

def edit_prompt(prompt: str, change_description: str, config: Optional[LLMConfig] = None) -> str:
    """Edit an existing prompt to improve its effectiveness.
    
    Args:
        prompt: The existing prompt to improve
        change_description: Description of the changes to make
        config: Optional LLM configuration. If not provided, uses default OpenAI config
        
    Returns:
        str: The improved prompt with reasoning analysis
    """
    from .prompts.system import PROMPT_EDITOR
    
    if config is None:
        config = LLMConfig.default_openai()
    
    client = LLMClient(config)
    return client.generate([
        {
            "role": "system",
            "content": PROMPT_EDITOR.content,
        },
        {
            "role": "user",
            "content": f"""Current Prompt:
{prompt}

Change Description:
{change_description}""",
        },
    ])

def create_audio_prompt(task_or_prompt: str, config: Optional[LLMConfig] = None) -> str:
    """Create a new prompt optimized for audio output based on a task description.
    
    Args:
        task_or_prompt: Description of the task or existing prompt to improve
        config: Optional LLM configuration. If not provided, uses default OpenAI config
        
    Returns:
        str: The generated audio-optimized prompt
    """
    from .prompts.system import AUDIO_PROMPT_GENERATOR
    
    if config is None:
        config = LLMConfig.default_openai()
    
    client = LLMClient(config)
    return client.generate([
        {
            "role": "system",
            "content": AUDIO_PROMPT_GENERATOR.content,
        },
        {
            "role": "user",
            "content": "Task, Goal, or Current Prompt:\n" + task_or_prompt,
        },
    ])

def edit_audio_prompt(prompt: str, change_description: str, config: Optional[LLMConfig] = None) -> str:
    """Edit an existing audio prompt to improve its effectiveness.
    
    Args:
        prompt: The existing prompt to improve
        change_description: Description of the changes to make
        config: Optional LLM configuration. If not provided, uses default OpenAI config
        
    Returns:
        str: The improved audio prompt with reasoning analysis
    """
    from .prompts.system import AUDIO_PROMPT_EDITOR
    
    if config is None:
        config = LLMConfig.default_openai()
    
    client = LLMClient(config)
    return client.generate([
        {
            "role": "system",
            "content": AUDIO_PROMPT_EDITOR.content,
        },
        {
            "role": "user",
            "content": f"""Current Prompt:
{prompt}

Change Description:
{change_description}""",
        },
    ])

def generate_audio_prompt(task_or_prompt: str, model: str = "gpt-4o") -> str:
    """Simple interface for generating audio-optimized prompts using OpenAI.
    
    This matches the interface of the example code while using our robust implementation.
    
    Args:
        task_or_prompt: The task description or existing prompt to improve
        model: The OpenAI model to use (default: "gpt-4o")
        
    Returns:
        str: The generated audio-optimized prompt
    """
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model=model,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return create_audio_prompt(task_or_prompt, config=config)

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
        model=model,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return create_prompt(task_or_prompt, config=config)

def generate_schema(description: str, model: str = "gpt-4") -> Dict:
    """Generate a JSON schema based on a description.
    
    Args:
        description: Description of the function to generate a schema for
        model: The model to use for generation
        
    Returns:
        Dict containing the generated schema
    """
    messages = [
        {"role": "system", "content": "Generate a JSON schema based on the following description:"},
        {"role": "user", "content": description}
    ]
    
    response = OpenAI.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.0,
        max_tokens=1000
    )
    
    schema_str = response.choices[0].message.content
    try:
        # Extract the schema from the response if it's wrapped in a code block
        if "```json" in schema_str:
            schema_str = schema_str.split("```json")[1].split("```")[0].strip()
        elif "```" in schema_str:
            schema_str = schema_str.split("```")[1].split("```")[0].strip()
            
        schema = json.loads(schema_str)
        return schema
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse generated schema: {e}")
