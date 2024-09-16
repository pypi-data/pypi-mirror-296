import os
import re
from tqdm import tqdm
from github import Github, GithubException
import git
import shutil

# Define a class to extract and process GitHub repository content
class GitHubRepoExtractor:
    # Initialize the extractor with repository details and authentication
    def __init__(self, repo_input, access_token=None, local_path=None):    
        self.repo_input = repo_input
        self.access_token = access_token
        self.local_path = local_path
        self.ignore_files = set()
        self.ignore_folders = set()
        self.ignore_extensions = set()
        self.include_files = set()
        self.include_extensions = set()
        # Define a set of binary file extensions that are typically not processed
        self.binary_extensions = {
            # Compressed archives
            '.zip', '.rar', '.7z', '.gz', '.tar', '.bz2',
            # Executables and libraries
            '.exe', '.dll', '.so', '.dylib', '.bin',
            # Java-related files
            '.jar', '.war', '.ear', '.class',
            # Image files
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.ico', '.svg', 
            '.webp', '.heic', '.heif', '.raw', '.cr2', '.nef', '.arw', '.dng',
            # Design and document files
            '.psd', '.ai', '.eps', '.indd',
            # Audio and video files
            '.mp3', '.mp4', '.avi', '.mov', '.flv', '.wav', '.ogg', '.mkv', '.webm',
            # Document files
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.bib',
            # Other common binary formats
            '.iso', '.img', '.db', '.sqlite', '.pyc', '.pyo',
            '.o', '.obj', '.a', '.lib',
            # Other formats
            '.stage'
        }
        self.total_files = 0
        self.processed_files = 0
        self.exclusive_mode = False
        self.is_local = local_path is not None
        
        # If a local path is provided, use it; otherwise, prepare to clone the repo
        if self.is_local:
            self.repo_path = local_path
        else:
            self.github = Github(access_token)
            self.repo = self.get_repo_from_input(repo_input)
            self.repo_path = None

    # Determine the repository based on the input format
    def get_repo_from_input(self, repo_input):
        # Handle different input formats: URL, 'owner/repo', or just 'repo' (for authenticated user)
        if repo_input.startswith('http'):
            # Extract owner/repo from the URL
            match = re.search(r'github.com/([^/]+)/([^/]+)(?:\.git)?', repo_input)
            if match:
                owner, repo = match.groups()
                repo = repo.replace('.git', '')
                print(f"Owner: {owner}, Repo: {repo}")
                return self.github.get_repo(f"{owner}/{repo}")
        elif '/' in repo_input:
            # Format 'owner/repo'
            return self.github.get_repo(repo_input)
        else:
            # Assume it's just the repo name for the authenticated user
            return self.github.get_user().get_repo(repo_input)
    
    # Clone the repository to a local path
    def clone_repo(self):
        if self.is_local:
            return

        print("Cloning repository...")
        repo_url = self.repo.clone_url
        # If an access token is provided, use it for cloning
        if self.access_token:
            repo_url = repo_url.replace('https://', f'https://{self.access_token}@')
        
        # Define a temporary directory for cloning
        self.repo_path = f"./temp_repo_{self.repo.name}"
        # Remove the directory if it already exists
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path)
        
        # Clone the repository
        git.Repo.clone_from(repo_url, self.repo_path)
        print(f"Repository cloned to {self.repo_path}")

    # Set the lists of files, folders, and extensions to ignore during processing
    def set_ignore_list(self, files=None, folders=None, extensions=None):
        self.ignore_files = set(files or [])
        self.ignore_folders = set(folders or [])
        self.ignore_extensions = set(extensions or []).union(self.binary_extensions)

    # Set the lists of files and extensions to include during processing, with an option for exclusive mode
    def set_include_list(self, files=None, extensions=None, exclusive=False):
        self.include_files = set(files or [])
        self.include_extensions = set(extensions or [])
        self.exclusive_mode = exclusive

    # Determine whether a file should be processed based on the include and ignore lists
    def should_process(self, path):
        file_name = os.path.basename(path)
        _, file_extension = os.path.splitext(file_name)
        
        # In exclusive mode, only process included files and extensions
        if self.exclusive_mode:
            return (file_name in self.include_files or 
                    file_extension.lower() in self.include_extensions)
        else:
            # Otherwise, ignore specified files, folders, and extensions
            if (file_name in self.ignore_files or
                any(folder in path.split(os.sep) for folder in self.ignore_folders) or
                file_extension.lower() in self.ignore_extensions):
                return False
            return True

    # Determine whether a file should be ignored based on the ignore lists
    def should_ignore(self, path):
        if os.path.basename(path) in self.ignore_files:
            return True
        if any(folder in path.split('/') for folder in self.ignore_folders):
            return True
        if any(path.lower().endswith(ext) for ext in self.ignore_extensions):
            return True
        return False
    
    # Count the total number of files to be processed in the repository
    def count_files(self, path=""):
        for root, dirs, files in os.walk(os.path.join(self.repo_path, path)):
            # Exclude ignored folders from the search
            dirs[:] = [d for d in dirs if d not in self.ignore_folders]
            for file in files:
                file_path = os.path.join(root, file)
                if self.should_process(file_path):
                    self.total_files += 1

    # Process the content of the repository and write it to an output file
    def process_content(self, path, output_file, progress_bar):
        for root, dirs, files in os.walk(os.path.join(self.repo_path, path)):
            # Exclude ignored folders from the search
            dirs[:] = [d for d in dirs if d not in self.ignore_folders]
            for file in files:
                file_path = os.path.join(root, file)
                if self.should_process(file_path):
                    try:
                        # Read the file content and write it to the output file
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        relative_path = os.path.relpath(file_path, self.repo_path)
                        output_file.write(f"# File: {relative_path}\n\n")
                        output_file.write(file_content)
                        output_file.write("\n\n")
                        self.processed_files += 1
                        progress_bar.update(1)
                    except UnicodeDecodeError:
                        # Warn if the file cannot be decoded, likely a binary file
                        print(f"Warning: Unable to decode {file_path}. It might be a binary file.")
                else:
                    # Skip files that should not be processed
                    print(f"Skipping: {file_path}")

    # Extract the repository content to a specified output file
    def extract_to_file(self, output_filename='output.txt'):
        try:
            # Clone the repository if it's not a local path
            if not self.is_local:
                self.clone_repo()

            print("Counting files in the repository...")
            self.count_files()
            print(f"Total files to process: {self.total_files}")

            # Open the output file and process the repository content
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                with tqdm(total=self.total_files, desc="Processing files") as progress_bar:
                    self.process_content("", output_file, progress_bar)

            # Report successful extraction
            print(f"Repository content has been successfully extracted to {output_filename}")
            print(f"Processed {self.processed_files} out of {self.total_files} files.")
        except Exception as e:
            # Handle any exceptions that occur during extraction
            print(f"An error occurred: {str(e)}")
        finally:
            # Clean up temporary files if the repository was cloned
            if not self.is_local and self.repo_path:
                print("Cleaning up temporary files...")
                shutil.rmtree(self.repo_path)

# Example usage
if __name__ == "__main__":
    access_token = input("Enter your GitHub access token: ")
    repo_full_name = input("Enter the full repository name (e.g., 'https://github.com/ltoscano/github-repo-extractor.git'): ")

    extractor = GitHubRepoExtractor(
        repo_input = repo_full_name, 
        access_token = access_token
        )
    
    # Example of setting additional ignore lists
    extractor.set_ignore_list(
        files=['.gitignore'],
        folders=['tests', '.github'],
        extensions=['.log']  # Additional extensions can be added here
    )

    # Example of setting include list
    extractor.set_include_list(
        files=['README.md'],
        extensions=['.java'],
        exclusive=True  # Set to True to only include these files/extensions
    )
    
    extractor.extract_to_file()
