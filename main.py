import os
import shutil
import typer
from github import Github, GithubException
from git import Repo

app = typer.Typer()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    typer.echo("Please set your GITHUB_TOKEN environment variable")
    raise typer.Exit(1)

g = Github(GITHUB_TOKEN)


LABELS = [
    {"name": "HELP", "color": "008672", "description": "Extra attention is needed"},
    {"name": "priority: critical", "color": "b60205", "description": ""},
    {"name": "priority: high", "color": "d93f0b", "description": ""},
    {"name": "priority: low", "color": "0e8a16", "description": ""},
    {"name": "priority: medium", "color": "fbca04", "description": ""},
    {"name": "type: bug", "color": "d73a4a", "description": "Something isn't working"},
    {"name": "type: discussion", "color": "d4c5f9", "description": ""},
    {"name": "type: documentation", "color": "006b75", "description": ""},
    {"name": "type: enhancement", "color": "84b6eb", "description": ""},
    {"name": "type: complex", "color": "3E4B9E", "description": "A theme of work that contain sub-tasks"},
    {"name": "type: feature request", "color": "fbca04", "description": "New feature or request"},
    {"name": "type: question", "color": "d876e3", "description": "Further information is requested"},
]

def create_labels(repo):
    existing_labels = {label.name for label in repo.get_labels()}
    for label in LABELS:
        if label["name"] not in existing_labels:
            try:
                repo.create_label(
                    name=label["name"],
                    color=label["color"],
                    description=label["description"],
                )
                typer.echo(f"🏷️ Created label: {label['name']}")
            except GithubException as e:
                typer.echo(f"Failed to create label {label['name']}: {e}")

def copy_workflow(temp_repo_path):
    """Copy safety.yml from current dir into the cloned repo workflow folder"""
    workflow_src = os.path.join(os.getcwd(), "safety.yml")
    workflow_dst_dir = os.path.join(temp_repo_path, ".github", "workflows")
    os.makedirs(workflow_dst_dir, exist_ok=True)
    shutil.copyfile(workflow_src, os.path.join(workflow_dst_dir, "safety.yml"))
    typer.echo("Copied safety.yml workflow file")

def protect_branch(repo, branch_name, required_reviewers):
    try:
        branch = repo.get_branch(branch_name)
        branch.edit_protection(
            required_approving_review_count=required_reviewers,
            enforce_admins=True,
            dismiss_stale_reviews=True,
            require_code_owner_reviews=True,
            restrictions=None,
            require_status_checks=False,
            contexts=[],
        )
        typer.echo(f"Branch protection enabled on '{branch_name}' requiring {required_reviewers} approvals")
    except GithubException as e:
        typer.echo(f"Could not protect branch '{branch_name}': {e}")

@app.command()
def duplicate_repo(original_url: str, new_name: str):
    user = g.get_user()
    typer.echo(f"🔍 Fetching original repo from URL: {original_url}")

    try:
        original_repo = g.get_repo(original_url.split("github.com/")[1])
    except Exception as e:
        typer.echo(f"Failed to get repo: {e}")
        raise typer.Exit(1)

    try:
        new_repo = user.create_repo(new_name, private=True)
        typer.echo(f"Created new repo: {new_name}")
    except GithubException as e:
        typer.echo(f"Failed to create repo: {e}")
        raise typer.Exit(1)

    temp_path = "temp_repo"
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    typer.echo(f"⏳ Cloning original repo locally to {temp_path}")
    Repo.clone_from(original_url, temp_path)

    repo = Repo(temp_path)
    repo.create_remote("target", new_repo.clone_url)

    typer.echo("Pushing all branches to new repo")
    repo.remote("target").push(refspec="refs/heads/*:refs/heads/*")
    copy_workflow(temp_path)
    repo.git.add(all=True)
    repo.index.commit("Add safety workflow")
    repo.remote("target").push()

    collaborators = list(original_repo.get_collaborators())
    for collab in collaborators:
        try:
            new_repo.add_to_collaborators(collab.login, permission="push")
            typer.echo(f"👥 Added collaborator: {collab.login}")
        except GithubException as e:
            typer.echo(f"⚠️ Failed to add collaborator {collab.login}: {e}")

    if user.login not in [c.login for c in collaborators]:
        new_repo.add_to_collaborators(user.login, permission="admin")
    create_labels(new_repo)
    collab_count = len(collaborators) + 1
    for branch_name in ["main", "dev"]:
        try:
            protect_branch(new_repo, branch_name, collab_count)
        except Exception as e:
            typer.echo(f"⚠️ Failed to protect branch {branch_name}: {e}")
    shutil.rmtree(temp_path)
    typer.echo("🧹 Cleaned up temporary files")
    typer.echo(f"🎉 Repo duplication complete! {new_name} is ready.")

if __name__ == "__main__":
    app()
