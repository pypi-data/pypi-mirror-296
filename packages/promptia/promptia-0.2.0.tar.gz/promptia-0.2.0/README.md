# Promptia

Promptia is a Python library designed to streamline the management and generation of prompts for Large Language Models (LLMs).

## Features

- Manage prompt templates for various LLMs and APIs
- Convert abstract templates to specific API formats
- Support for function calling with detailed configurations
- Version control for templates
- Dynamic information embedding using Retrieval-Augmented Generation (RAG)
- Modular design for flexibility and extensibility

## Installation

```
pip install promptia[openai]
```

## Quick Start

```python
from promptia import Promptia, MemoryStorage, OpenAIGPT4oMini

# Initialize Promptia
manager = Promptia(MemoryStorage())

# Add a template
manager.add_template(
    name="greeting",
    content="Hello, {name}! Welcome to {place}.",
    parameters={"name": "string", "place": "string"}
)

# Build and use a prompt
prompt = manager.build("greeting", "1.0", {"name": "Alice", "place": "Wonderland"})
result = OpenAIGPT4oMini.call_llm(prompt)

print(result)
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
