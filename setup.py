from setuptools import setup, find_packages

setup(
    name="promptlibrary",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "openai>=1.0.0",
        "ollama>=0.1.0",
        "jsonschema>=4.20.0",
        "pydantic>=2.5.0",
        "typing-extensions>=4.8.0",
        "python-dotenv>=1.0.0"
    ],
    author="Jacques Murray",
    author_email="jacquesmmurray@gmail.com",
    description="A library for managing and organizing prompts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jacques-Murray/promptlibrary",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
