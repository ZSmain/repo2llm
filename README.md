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

### Project Type

You can tailor file inclusion for specific project types using the `--project-type` (or `-p`) argument:

```bash
repo2llm /path/to/repository -p django
```

- **Purpose**: This option helps include files typically relevant to the specified project type.
- **Available choices**: `django`, `sveltekit`.
- **Default behavior**: If `--project-type` is not provided, a general set of common file extensions will be used.

**File Extensions Included:**

-   **Django (`-p django`)**:
    `['.py', '.html', '.css', '.js', '.json', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.po', '.mo']`
-   **SvelteKit (`-p sveltekit`)**:
    `['.svelte', '.js', '.ts', '.html', '.css', '.json', '.yml', '.yaml', '.md']`
-   **Default (no project type specified)**:
    `['.py', '.js', '.txt', '.md', '.html', '.css', '.json', '.yml', '.yaml', '.xml', '.toml', '.ini', '.cfg', '.svelte', '.ts']`

### Customizing Included Files

You can also explicitly specify which file extensions to include using the `--include-extensions` argument (not yet implemented).

**Interaction of `--project-type` and `--include-extensions`**:

If the `--include-extensions` argument is provided, it will override any file extension list that would have been determined by `--project-type` or the default settings. This gives you precise control over which file types are consolidated.

By default, repo2llm:
- Excludes common directories like `.git`, `__pycache__`, `migrations`, `tests`, `.venv` etc. (Note: the specific list of excluded directories can be seen in the `consolidate_files` function in `src/repo2llm/__init__.py`).
- Filters files based on the `--project-type`, `--include-extensions`, or default settings as described above.