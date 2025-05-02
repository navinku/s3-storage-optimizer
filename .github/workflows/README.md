# GitHub to GitLab Sync Automation

## 📌 Overview
This GitHub Action automatically mirrors pushes to the `main` branch from GitHub to a GitLab repository. Designed for projects using GitHub as the primary source but requiring GitLab for CI/CD pipelines.

```mermaid
graph LR
    A[GitHub Push to main] --> B[GitHub Action Trigger]
    B --> C[Checkout Repository]
    C --> D[Configure Git Settings]
    D --> E[Add GitLab Remote]
    E --> F[Push to GitLab]
    F --> G[GitLab Repo Updated]
```

## ⚙️ Workflow Configuration
```yaml
name: Sync to GitLab
on:
  push:
    branches: [main]
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history clone

      - name: Sync to GitLab
        env:
          GITLAB_TOKEN: ${{ secrets.GITLAB_TOKEN }}
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git remote add gitlab https://oauth2:${GITLAB_TOKEN}@gitlab.com/githubsync2/s3-storage-optimizer.git
          git push gitlab main
```

## 🔑 Setup Instructions

### 1. GitLab Token Preparation
1. Create a GitLab access token with:
   - `api` and `write_repository` scopes
   - No expiration (or set appropriate duration)

2. Add to GitHub Secrets:
   - Go to: GitHub Repo → Settings → Secrets → Actions
   - Create secret named `GITLAB_TOKEN` with the token value

### 2. Repository Path Configuration
- Update the GitLab remote URL in the workflow:
  ```diff
  - git remote add gitlab https://oauth2:${GITLAB_TOKEN}@gitlab.com/githubsync2/s3-storage-optimizer.git
  + git remote add gitlab https://oauth2:${GITLAB_TOKEN}@gitlab.com/YOUR_GROUP/YOUR_PROJECT.git
  ```

## 🔄 Push Behavior Options
| Command | Behavior |
|---------|----------|
| `git push gitlab main` | Standard push |
| `git push --force gitlab main` | Force push (overwrites remote) |
| `git push gitlab main:sync-main` | Pushes to different branch |

## 🛠️ Troubleshooting

### Common Issues
1. **Authentication Errors**:
   - Verify token has correct scopes
   - Try alternative auth prefix:
     ```diff
     - https://oauth2:${GITLAB_TOKEN}@
     + https://gitlab-ci-token:${GITLAB_TOKEN}@
     ```

2. **Permission Denied**:
   - Confirm the token owner has push access to the GitLab repo

3. **Shallow Clone Issues**:
   - Ensure `fetch-depth: 0` is set in checkout action

## 📂 Recommended Repository Structure
```
.github/
└── workflows/
    ├── sync-to-gitlab.yml   # This workflow
    ├── README.md            # This documentation
    └── ...other workflows
```

## 🔍 Monitoring
Check sync status in:
1. GitHub Actions tab → "Sync to GitLab" workflow runs
2. GitLab repository → Commits history

---

**Note**: For mission-critical syncs, consider adding error notifications via Slack/Email in the workflow.
```

Key features:
1. Visual workflow diagram showing the entire process
2. Ready-to-use YAML configuration
3. Detailed setup instructions
4. Troubleshooting guide
5. Multiple push options comparison
6. Clean documentation structure