# Project Name

## Description

Brief description of the project (en anglais svp).

---

## Folder Structure

```plaintext
project-name
├── build/
│   └── Dockerfile               # Build using Docker for Ubuntu 24.04 testing
├── src/
│   └── ...                      # Source files
├── .github/
│   └── workflows/
│       ├── safety-checks.yml    # Pipeline to check if all requirements are there in order to push
│       └── release.yml          # Pipeline that does versioning by creating releases of the project
└── README.md
```

## Commit Norm

We use a clear and consistent commit norm inspired by [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) :

```plaintext
<type>(<field>): <description>
```

### Types include:

- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Code style or formatting changes (no logic changes)
- refactor: Code changes that neither fix a bug nor add a feature
- test: Adding or fixing tests
- build: Changes that affect the build system or external dependencies

Example:
```plaintext
feat(Setup/Build): Added the docker build folder as well as the GitHub Actions workflow
```

## Branching & Labels

### Issue-Based Branch Naming

Each feature, bugfix, or task starts from a GitHub issue.

When starting work on an issue:

- **Create a new branch directly from the issue page on GitHub**
- The branch will follow this naming convention:  
```plaintext
<issue-number>-<short-title-explaining-the-issue>
```

Usually, the branch name is made by Github after the title of the issue.

**Examples:**

- `12-nombres-négatifs-pas-de-gestion-d'erreur`
- `7-implémentation-d'un-algorithme-de-tri`
- `42-problemes-de-coding-style`

This keeps branches linked to their issues for better traceability.

---

### 🏷️ Labeling Convention

Each issue can be attributed labels to explain what it is about:

| Label           | Description                                  |
|-----------------|----------------------------------------------|
| `Bug`           | Something doesn’t work as expected           |
| `Feature`       | A new functionality to add                   |
| `Coding Style`  | Coding Style Problems                        |
| `Tests`         | Add or improve tests                         |
| `Documentation` | Doc updates or improvements                  |
| `Refactor`      | Code restructuring without behavior changes  |
| `Bizarre`       | Something feels weird, needs another look    |
| `HELP`          | Request for help or collaboration            |
| `In Progress`   | Currently doing                              |
| `Performance`   | Upgrading the performance                    |

## Setup and Running

### Install the dependencies

```sh
echo 'Our dependencies'
```

### Running

```sh
echo 'How to run it'
```

## Collaborators

Thanks to everyone who contributed:

[Collaborator's Name](https://github.com/name)  
[Collaborator's Name](https://github.com/name)  
[Collaborator's Name](https://github.com/name)  
