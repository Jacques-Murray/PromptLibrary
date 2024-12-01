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
3. Install pre-commit hooks: `pre-commit install`
4. Run tests: `pytest tests/`

### Code Quality

This project uses several tools to maintain code quality:

- **pre-commit hooks** for automated code formatting and checks
  - Black (code formatter)
  - isort (import sorter)
  - flake8 (linter)
  - mypy (type checker)

### CI/CD

We use GitHub Actions for continuous integration and deployment:

- **Test Workflow**: Runs on every push and pull request
  - Executes test suite with pytest
  - Runs pre-commit checks
  - Generates coverage reports
  - Requires Python 3.11+

- **Security Scanning**: Weekly and on code changes
  - Uses GitHub CodeQL
  - Performs security and quality analysis
  - Focuses on Python-specific vulnerabilities

- **Publishing**: Automated on new releases
  - Builds and publishes to PyPI
  - Includes verification steps
  - Uses trusted publishing

## Requirements

- Python >= 3.11
- OpenAI API key for GPT model access
- See requirements.txt for full dependency list
