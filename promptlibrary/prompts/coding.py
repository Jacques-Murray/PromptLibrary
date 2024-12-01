from ..models import Prompt, PromptCategory

CODE_REVIEW_PROMPT = Prompt(
    name="code_review",
    category=PromptCategory.CODING,
    description="A prompt for conducting code reviews",
    template="""Please review the following code for:
1. Potential bugs
2. Performance issues
3. Best practices
4. Security concerns

Code to review:
{code}

Additional context:
{context}
""",
    tags=["review", "code quality", "security"],
    model_compatibility=["gpt-4", "gpt-3.5-turbo"],
    parameters={
        "code": "The code to review",
        "context": "Additional context about the code"
    }
)
