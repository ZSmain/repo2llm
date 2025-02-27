import os
import argparse
from pathlib import Path

def consolidate_files(repo_path: str, output_file: str, exclude_dirs: list[str] | None = None, 
                     include_extensions: list[str] | None = None) -> None:
    """
    Consolidates all files in a repository into a single text file.
    
    Args:
        repo_path (str): Path to the root of the repository.
        output_file (str): Path to the output file.
        exclude_dirs (list): Directories to exclude from processing.
        include_extensions (list): File extensions to include for consolidation.
    """
    exclude_dirs = exclude_dirs or ['.git', '__pycache__', 'migrations', 'tests', '.venv']
    include_extensions = include_extensions or ['.py', '.js', '.txt', '.md', '.html', '.css']
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(repo_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in include_extensions):
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
        default="consolidated_repository.txt",
        help="Output file path (default: consolidated_repository.txt)"
    )
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.is_dir():
        print(f"Error: {repo_path} is not a valid directory")
        return
    
    print(f"Processing repository: {repo_path}")
    print(f"Output file: {args.output}")
    
    consolidate_files(str(repo_path), args.output)
    print("Repository consolidation complete!")
