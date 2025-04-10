# repo2llm

A simple CLI tool to convert a repository into a single text file for language model processing.

## Installation

You can install repo2llm using the `uv` tool:

```bash
uv tool install . -e
```

## Usage

Basic usage:

```bash
repo2llm /path/to/repository
```

This will create a text file in the current directory with the format `repository_name_llm_YYYY-MM-DD.txt`.

Options:

```bash
repo2llm /path/to/repository -o output_file.txt
```

By default, repo2llm:
- Excludes common directories like `.git`, `__pycache__`, etc.
- Only includes files with common extensions like `.py`, `.js`, `.txt`, `.md`, etc.