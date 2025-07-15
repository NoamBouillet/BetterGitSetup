# BetterGitSetup

BetterGitSetup is a CLI tool that helps you automate GitHub repository duplication, setup, and lightweight ticketing-like workflows.

## Features
- Duplicate a GitHub repository (push all branches)
- Copy collaborators from the original repository automatically
- Setup GitHub Actions by copying a workflow YAML file
- Create labels for issue tracking (priority, types, etc.)
- Add Git tags
- Protect branches (main, dev) with PR review requirements

## Requirements
- Python 3.8+
- A GitHub **Personal Access Token** (PAT) with `repo`, `admin:repo_hook`, `write:org`, and `workflow` scopes

## Installation
```bash
pip install -r requirements.txt
```

## Folder Structure
```
bettergit/
├── setup.py
├── .env.example
├── CONVENTIONAL-README.md    # The flexible Readme to copy into the new repository
├── safety.yml
├──/build
   ├── Dockerfile
```

## Setup
1. Copy `.env.example` to `.env` and add your GitHub token:
```bash
cp .env.example .env
```

2. Fill in your token:
```
GITHUB_TOKEN=ghp_your_personal_token_here
```

## How to Get a GitHub Token
1. Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Set expiration and scopes:
   - ✅ `repo`
   - ✅ `admin:repo_hook`
   - ✅ `workflow`
   - ✅ `write:org`
4. Copy and store your token securely (you won't see it again!)

## GitHub Secrets to Set (on the duplicated repo)
After duplication, make sure to set these secrets in the **new repository's** Settings > Secrets:
- `GIT_SSH_PRIVATE_KEY` → Your private SSH key (for repo mirroring)
- (Optional) `EXECUTABLES` → Comma-separated names of executables for the `make` check

## Usage
```bash
python setup.py https://github.com/username/original-repo new-repo-name
```

## Labels
Automatically adds the following labels to the new repo:
- `HELP`
- `priority: critical | high | medium | low`
- `type: bug | enhancement | feature request | documentation | question | discussion | complex`

## Protections
- Sets up **branch protection** on `main` and `dev`
- Requires **all collaborators to approve** PRs before merging into `main` and `dev`

## License
MIT License
