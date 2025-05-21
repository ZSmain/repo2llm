import os
import argparse
from pathlib import Path
from datetime import datetime

def consolidate_files(repo_path: str, output_file: str = None, exclude_dirs: list[str] | None = None, 
                     include_extensions: list[str] | None = None, project_type: str | None = None) -> None:
    """
    Consolidates all files in a repository into a single text file.
    
    Args:
        repo_path (str): Path to the root of the repository.
        output_file (str): Path to the output file. If None, a name will be generated.
        exclude_dirs (list): Directories to exclude from processing.
        include_extensions (list): File extensions to include for consolidation.
        project_type (str, optional): Type of project (e.g., 'django', 'sveltekit') to determine default extensions.
    """
    exclude_dirs = exclude_dirs or ['.git', '__pycache__', 'migrations', 'tests', '.venv']
    
    PROJECT_EXTENSIONS = {
        'django': ['.py', '.html', '.css', '.js', '.json', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.po', '.mo'],
        'sveltekit': ['.svelte', '.js', '.ts', '.html', '.css', '.json', '.yml', '.yaml', '.md'],
    }
    DEFAULT_EXTENSIONS = ['.py', '.js', '.txt', '.md', '.html', '.css', '.json', '.yml', '.yaml', '.xml', '.toml', '.ini', '.cfg', '.svelte', '.ts']

    if include_extensions is not None:
        effective_extensions = include_extensions
    elif project_type and project_type in PROJECT_EXTENSIONS:
        effective_extensions = PROJECT_EXTENSIONS[project_type]
    else:
        effective_extensions = DEFAULT_EXTENSIONS
        
    # Generate default filename if not provided
    if output_file is None:
        # Extract project name from repo path
        project_name = os.path.basename(os.path.normpath(repo_path))
        # Get current date in YYYY-MM-DD format
        current_date = datetime.now().strftime("%Y-%m-%d")
        # Create filename
        output_file = f"{project_name}_llm_{current_date}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(repo_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in effective_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"## FILE: {file_path}\n\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")
                    except Exception as e:
                        print(f"Could not read file {file_path}: {e}")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a repository into a single text file for language model processing"
    )
    parser.add_argument("repo_path", help="Path to the repository to process")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file path (default: PROJECT_NAME_llm_YYYY-MM-DD.txt)"
    )
    parser.add_argument(
        "-p",
        "--project-type",
        choices=['django', 'sveltekit'],
        help="Type of project to process (django or sveltekit)"
    )
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.is_dir():
        print(f"Error: {repo_path} is not a valid directory")
        return
    
    print(f"Processing repository: {repo_path}")
    
    if args.output is None:
        # Extract project name from repo path
        project_name = repo_path.name
        # Get current date in YYYY-MM-DD format
        current_date = datetime.now().strftime("%Y-%m-%d")
        # Create filename
        output_file = f"{project_name}_llm_{current_date}.txt"
    else:
        output_file = args.output
    
    print(f"Output file: {output_file}")
    
    consolidate_files(str(repo_path), output_file, project_type=args.project_type)
    print("Repository consolidation complete!")
