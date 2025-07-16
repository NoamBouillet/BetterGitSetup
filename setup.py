import os
import shutil
import tempfile
from git import Repo
from github import Github
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN not found in environment.")

def authenticated_url(original_url):
    parsed = urlparse(original_url)
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are supported for authentication.")
    netloc = f"{token}@{parsed.netloc}"
    return urlunparse(parsed._replace(netloc=netloc))

def duplicate_repo(original_url, new_name, tag=None):
    tmp_dir = tempfile.mkdtemp()
    print(f"Cloning from {original_url}...")
    Repo.clone_from(authenticated_url(original_url), tmp_dir)

    print(f"Creating repo {new_name} on GitHub...")
    gh = Github(token)
    user = gh.get_user()
    new_repo = user.create_repo(new_name, private=True)
    repo = Repo(tmp_dir)

    if 'new_origin' in [r.name for r in repo.remotes]:
        new_remote = repo.remotes.new_origin
        new_remote.set_url(authenticated_url(new_repo.clone_url))
    else:
        new_remote = repo.create_remote('new_origin', authenticated_url(new_repo.clone_url))

    print("Pushing all refs to new_origin with --mirror...")
    repo.git.push('--mirror', 'new_origin')

    print("Deleting default labels...")
    for label in new_repo.get_labels():
        try:
            label.delete()
        except Exception as e:
            print(f"Warning: Couldn't delete label {label.name}: {e}")

    print("Adding custom labels...")
    labels = [
        {"name": "HELP", "color": "008672", "description": "Extra attention is needed"},
        {"name": "priority: critical", "color": "b60205", "description": ""},
        {"name": "priority: high", "color": "d93f0b", "description": ""},
        {"name": "priority: medium", "color": "fbca04", "description": ""},
        {"name": "priority: low", "color": "0e8a16", "description": ""},
        {"name": "type: bug", "color": "d73a4a", "description": "Something isn't working"},
        {"name": "type: discussion", "color": "d4c5f9", "description": ""},
        {"name": "type: documentation", "color": "006b75", "description": ""},
        {"name": "type: enhancement", "color": "84b6eb", "description": ""},
        {"name": "type: complex", "color": "3E4B9E", "description": "A theme of work that contain sub-tasks"},
        {"name": "type: feature request", "color": "fbca04", "description": "New feature or request"},
        {"name": "type: question", "color": "d876e3", "description": "Further information is requested"},
    ]

    for label in labels:
        try:
            new_repo.create_label(**label)
        except Exception as e:
            print(f"Warning: Couldn't create label {label['name']}: {e}")

    print("Copying GitHub Actions workflow...")
    workflows_path = os.path.join(tmp_dir, ".github", "workflows")
    os.makedirs(workflows_path, exist_ok=True)
    safety_yml_path = os.path.abspath("safety-checks.yml")
    shutil.copy(safety_yml_path, workflows_path)
    safety_readme_path = os.path.abspath("CONVENTIONAL-README.md")
    target_readme_path = os.path.join(tmp_dir, "README.md")
    shutil.copy(safety_readme_path, target_readme_path)

    repo.git.add(A=True)
    repo.index.commit("feat(Setup/Build): Added the docker build folder as well as the GitHub Actions workflow; also added a basic README")
    repo.git.push('new_origin', 'main')

    if tag:
        print(f"Tagging with {tag}...")
        repo.create_tag(tag)
        repo.git.push('new_origin', tag)
    print("Done.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("original_url")
    parser.add_argument("new_name")
    parser.add_argument("--tag", required=False)
    args = parser.parse_args()

    duplicate_repo(args.original_url, args.new_name, args.tag)
