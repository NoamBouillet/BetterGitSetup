# BetterGitSetup
BetterGitSetup is a CLI tool that automates GitHub repository duplication, setup, labeling, protections, and simplified ticket-based workflows.

## Features
- **Full repo duplication** with all branches and tags
- **GitHub Actions** workflow (e.g. coding style, compilation, testing)
- **Automatic label management** (delete defaults, create custom ones)
- **Branch protection rules** on `main` and `dev`
- **Release automation** (`.zip` archive from latest commits on main)

## Requirements
- Python 3.8+
- A GitHub **Personal Access Token** (PAT) with the following scopes:
  - `repo`
  - `admin:repo_hook`
  - `workflow`
  - `write:org`

## Installation
```bash
pip install -r requirements.txt
```

## Folder Structure
```
bettergit/
├── setup.py
├── .env.example
├── CONVENTIONAL-README.md
├── README.md
├── safety.yml
├── release.yml
├── requirements.txt
└──/build
   └── Dockerfile
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
