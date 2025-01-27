import os

def consolidate_files(repo_path, output_file, exclude_dirs=None, include_extensions=None):
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

if __name__ == "__main__":
    # Path to the root of your repository
    repo_path = "/path/to/repository"
    
    # Path to the consolidated output file
    output_file = "consolidated_repository.txt"
    
    consolidate_files(repo_path, output_file)
