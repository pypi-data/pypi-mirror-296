# LLM Assistant Framework

LLM Assistant Framework is a flexible and powerful Python library for building AI assistants using various Large Language Models (LLMs). Inspired by OpenAI's Assistants API, this framework allows you to create, manage, and interact with AI assistants using different LLM providers.

## Features

- 🚀 Easy-to-use API for creating and managing AI assistants
- 🔌 Flexible integration with multiple LLM providers
- 💬 Thread-based conversation management
- 🏃‍♂️ Asynchronous execution of assistant runs
- 🛠️ Customizable and extensible architecture

## Installation

You can install the LLM Assistant Framework using pip:

```bash
pip install llm-assistant-framework
```

## Usage

```python
from llm_assistant_framework import AssistantManager, ThreadManager, RunManager

# Initialize managers
assistant_manager = AssistantManager()
thread_manager = ThreadManager()
run_manager = RunManager(assistant_manager, thread_manager)

# Create an assistant with the custom LLM function
assistant = await assistant_manager.create_assistant(
    name="Sky Expert",
    instructions="You are an expert on atmospheric phenomena.",
    model="llama3",
    custom_llm_function=custom_llm_function,
    temperature=0.7,  # Additional parameter for the LLM
)
print(assistant)

# Create a thread
thread = await thread_manager.create_thread()
print(thread)
```

## Contributing

We welcome contributions to the LLM Assistant Framework! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
