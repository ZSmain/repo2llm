# repo2llm

A simple CLI tool to convert a repository into a single text file for language model processing.

## Installation

You can install repo2llm using bun:

```bash
bun install -g .
```

Or for development:

```bash
bun install
bun run build
bun link
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

- Respects the project's `.gitignore` file and excludes all patterns listed in it
- Additionally excludes common directories like `.git`, `node_modules`, `.venv`, etc. (even if not in .gitignore)
- Only includes files with common extensions like `.py`, `.js`, `.ts`, `.txt`, `.md`, etc.