from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm-assistant-framework",
    version="0.1.0",
    author="Lahfir",
    author_email="nmhlahfir2@gmail.com",
    description="A flexible framework for building AI assistants using various LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lahfir/llm-assistant-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp",
        "pydantic>=2.0.0",
        "fastapi",
    ],
)
