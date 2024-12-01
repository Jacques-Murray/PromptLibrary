# PromptLibrary

A Python package for managing and organizing prompts with support for schema validation and structured outputs.

## Features

- Generate and validate JSON schemas for function definitions
- Create and edit prompts with built-in validation
- Support for audio prompts and structured outputs
- Integration with OpenAI and Ollama models

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from promptlibrary import generate_schema, Schema

# Generate a JSON schema from description
schema = generate_schema("Create a function that takes a user's name and age")

# Create a schema manually
from promptlibrary import SchemaProperty
user_schema = Schema(
    name="create_user",
    description="Create a new user with name and age",
    properties={
        "name": SchemaProperty(type_="string", description="User's full name"),
        "age": SchemaProperty(type_="number", description="User's age in years")
    }
)
```

## Development

To contribute to this project:

1. Clone the repository
2. Install development dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest tests/`

## Requirements

- Python >= 3.11
- OpenAI API key for GPT model access
- See requirements.txt for full dependency list
