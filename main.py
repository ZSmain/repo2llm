import os

def concatenate_repo_to_single_file(repo_path, output_file, exclude_dirs=None, include_extensions=None):
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__', 'node_modules']  # Common directories to exclude
    if include_extensions is None:
        include_extensions = ['.py', '.js', '.txt', '.md', '.html', '.css']  # File types to include

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(repo_path):
            # Exclude specified directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if any(file.endswith(ext) for ext in include_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"=== File: {file_path} ===\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")
                    except UnicodeDecodeError:
                        print(f"Skipping binary or non-text file: {file_path}")


if __name__ == "__main__":

    # Example usage
    concatenate_repo_to_single_file('/path/to/repository', 'output.txt')
