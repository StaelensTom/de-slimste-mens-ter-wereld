"""
GitHub synchronization module for persisting question sets.
Commits changes directly to the GitHub repository.
"""
import os
import json
import base64
from github import Github, GithubException, InputGitTreeElement


class GitHubSync:
    """Handle GitHub repository synchronization for question sets."""
    
    def __init__(self):
        """Initialize GitHub client with token from environment."""
        self.token = os.environ.get('GITHUB_TOKEN')
        self.repo_name = os.environ.get('GITHUB_REPO')  # e.g., 'StaelensTom/de-slimste-mens-ter-wereld'
        self.branch = os.environ.get('GITHUB_BRANCH', 'main')
        
        self.enabled = bool(self.token and self.repo_name)
        
        if self.enabled:
            try:
                self.github = Github(self.token)
                self.repo = self.github.get_repo(self.repo_name)
            except Exception as e:
                print(f"GitHub sync disabled: {e}")
                self.enabled = False
    
    def commit_file(self, file_path, content, commit_message):
        """
        Commit a file to GitHub repository.
        
        Args:
            file_path: Path relative to repo root (e.g., 'default/3-6-9.json')
            content: File content as string or dict (will be JSON encoded if dict)
            commit_message: Commit message
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.enabled:
            print("GitHub sync is disabled (missing GITHUB_TOKEN or GITHUB_REPO)")
            return False
        
        try:
            # Convert dict to JSON string if needed
            if isinstance(content, dict) or isinstance(content, list):
                content = json.dumps(content, indent=2, ensure_ascii=False)
            
            # Try to get existing file
            try:
                existing_file = self.repo.get_contents(file_path, ref=self.branch)
                # Update existing file
                self.repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    sha=existing_file.sha,
                    branch=self.branch
                )
                print(f"✅ Updated {file_path} in GitHub")
            except GithubException as e:
                if e.status == 404:
                    # File doesn't exist, create it
                    self.repo.create_file(
                        path=file_path,
                        message=commit_message,
                        content=content,
                        branch=self.branch
                    )
                    print(f"✅ Created {file_path} in GitHub")
                else:
                    raise
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to commit {file_path} to GitHub: {e}")
            return False
    
    def commit_directory(self, directory_path, commit_message):
        """
        Commit an entire directory to GitHub in a single commit using Git Tree API.
        
        Args:
            directory_path: Local directory path
            commit_message: Commit message
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            print(f"🔄 Starting commit of directory: {directory_path}")
            
            # Get the latest commit SHA
            ref = self.repo.get_git_ref(f'heads/{self.branch}')
            latest_commit_sha = ref.object.sha
            base_tree = self.repo.get_git_commit(latest_commit_sha).tree
            print(f"  ✅ Got base tree from commit {latest_commit_sha[:7]}")
            
            # Collect all files to commit
            tree_elements = []
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    local_path = os.path.join(root, file)
                    # Get path relative to current directory
                    rel_path = os.path.relpath(local_path, '.').replace('\\', '/')
                    
                    # Read file content (handle both text and binary)
                    try:
                        with open(local_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        # Create blob for text file
                        blob = self.repo.create_git_blob(content, "utf-8")
                    except UnicodeDecodeError:
                        # Binary file - read as bytes and encode as base64
                        with open(local_path, 'rb') as f:
                            content = base64.b64encode(f.read()).decode('utf-8')
                        blob = self.repo.create_git_blob(content, "base64")
                    
                    # Add to tree elements
                    tree_elements.append(
                        InputGitTreeElement(
                            path=rel_path,
                            mode='100644',  # Regular file
                            type='blob',
                            sha=blob.sha
                        )
                    )
                    print(f"  📄 Prepared {rel_path}")
            
            if not tree_elements:
                print(f"⚠️ No files found in {directory_path}")
                return False
            
            print(f"  📦 Creating tree with {len(tree_elements)} files...")
            
            # Create new tree
            new_tree = self.repo.create_git_tree(tree_elements, base_tree)
            print(f"  ✅ Tree created: {new_tree.sha[:7]}")
            
            # Create commit
            parent = self.repo.get_git_commit(latest_commit_sha)
            new_commit = self.repo.create_git_commit(
                message=commit_message,
                tree=new_tree,
                parents=[parent]
            )
            print(f"  ✅ Commit created: {new_commit.sha[:7]}")
            
            # Update reference (with retry for race conditions)
            try:
                ref.edit(new_commit.sha)
                print(f"  ✅ Reference updated to {new_commit.sha[:7]}")
            except GithubException as e:
                if e.status == 422 and "not a fast forward" in str(e):
                    print(f"  ⚠️ Race condition detected, retrying with force update...")
                    ref.edit(new_commit.sha, force=True)
                    print(f"  ✅ Reference force-updated to {new_commit.sha[:7]}")
                else:
                    raise
            
            print(f"✅ Committed {len(tree_elements)} files from {directory_path} to GitHub in single commit")
            return True
            
        except Exception as e:
            import traceback
            print(f"❌ Failed to commit directory {directory_path}: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return False


# Global instance
github_sync = GitHubSync()
