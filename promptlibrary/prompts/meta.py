from ..models import Prompt, PromptCategory

META_PROMPT = Prompt(
    name="meta_prompt",
    category=PromptCategory.SYSTEM,
    description="A meta prompt for generating other prompts",
    template="""Create a prompt that achieves the following objective:
{objective}

The prompt should:
1. Be clear and specific
2. Include necessary context and constraints
3. Guide the model towards the desired output format
4. Include any relevant examples if needed

Additional requirements:
{requirements}

Target audience: {audience}
Expected output format: {output_format}""",
    tags=["meta", "prompt-generation"],
    model_compatibility=["gpt-4", "gpt-3.5-turbo"],
    parameters={
        "objective": "The main goal of the prompt to be generated",
        "requirements": "Any specific requirements or constraints",
        "audience": "The intended audience (e.g., 'LLM model', 'human reviewer')",
        "output_format": "Expected format of the response"
    }
)

def generate_prompt(
    objective: str,
    requirements: str = "None specified",
    audience: str = "LLM model",
    output_format: str = "Free text response"
) -> str:
    """
    Generate a new prompt using the meta prompt.
    
    Args:
        objective: The main goal of the prompt to be generated
        requirements: Any specific requirements or constraints
        audience: The intended audience
        output_format: Expected format of the response
    
    Returns:
        str: The generated prompt text
    """
    return META_PROMPT.format(
        objective=objective,
        requirements=requirements,
        audience=audience,
        output_format=output_format
    )
