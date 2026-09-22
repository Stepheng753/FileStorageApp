# Tooth Manager - CI/CD Pipeline & GitHub Actions Guide

Tooth Manager includes an automated GitHub Actions CI/CD pipeline configured at [`.github/workflows/deploy.yml`](file:///home/stepheng753/Development/FileStorageApp/.github/workflows/deploy.yml).

Every commit pushed to the `main` branch automatically runs automated tests, connects securely to the production VPS via SSH, deploys code updates, preserves all uploaded static documents, reloads Gunicorn, and verifies API health.

---

## 1. Setting Up SSH Keys & GitHub Secrets

Follow these steps once to authorize GitHub Actions to deploy to the production VPS (`69.62.71.85`).

### Step 1: Generate an SSH Key Pair
Run this command in your local terminal or WSL:
```bash
ssh-keygen -t ed25519 -C "github-actions-toothmanager" -f ~/.ssh/toothmanager_deploy
```
*When prompted for a passphrase, press **Enter** (no passphrase) so GitHub Actions can run non-interactively.*

This generates two files in `~/.ssh/`:
- `toothmanager_deploy`: Private key (secret)
- `toothmanager_deploy.pub`: Public key

---

### Step 2: Install the Public Key on the Production VPS
Copy the public key to your VPS user's `authorized_keys` file:

```bash
sshpass -p 7530 ssh-copy-id -i ~/.ssh/toothmanager_deploy.pub stepheng753@69.62.71.85
```

Alternatively, manually SSH into the VPS and append the contents of `toothmanager_deploy.pub` into `/home/stepheng753/.ssh/authorized_keys`:
```bash
cat ~/.ssh/toothmanager_deploy.pub | sshpass -p 7530 ssh stepheng753@69.62.71.85 "cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

---

### Step 3: Test Passwordless SSH Access
Verify that you can connect without entering the `7530` password:
```bash
ssh -i ~/.ssh/toothmanager_deploy stepheng753@69.62.71.85
```
If you log directly into the shell prompt (`stepheng753@srv805154`), the key setup is working!

---

### Step 4: Configure GitHub Secrets
1. Navigate to your GitHub repository in your browser:  
   `https://github.com/Stepheng753/FileStorageApp`
2. Go to **Settings** ➔ **Secrets and variables** ➔ **Actions**.
3. Click **New repository secret** and add the following 4 secrets:

| Secret Name | Value | Description |
| :--- | :--- | :--- |
| `PROD_HOST` | `69.62.71.85` | Public IP of the VPS |
| `PROD_USERNAME` | `stepheng753` | SSH user |
| `PROD_SSH_KEY` | *(Contents of `~/.ssh/toothmanager_deploy`)* | Full private key text including `-----BEGIN OPENSSH PRIVATE KEY-----` |
| `PROD_PORT` | `22` | Standard SSH port |

To easily display and copy your private key:
```bash
cat ~/.ssh/toothmanager_deploy
```

---

## 2. Pipeline Execution Stages

The workflow performs two sequential jobs:

```mermaid
graph LR
    Push["git push origin main"] --> TestJob["Job 1: Run Pytest Suite"]
    TestJob -->|Passes| DeployJob["Job 2: SSH Deploy to VPS"]
    DeployJob --> GitPull["Pull Latest main"]
    GitPull --> Deps["pip install -r requirements.txt"]
    Deps --> StorageGuard["Verify Storage & Permissions"]
    StorageGuard --> RestartGunicorn["sudo systemctl restart gunicorn"]
    RestartGunicorn --> HealthCheck["curl /api/health"]
```

### Protection of Uploaded Files:
- The deployment process executes `git reset --hard origin/main`.
- Because `Backend/static/*` is in `.gitignore`, **Git never deletes or alters uploaded practice documents**!
- The SQLite database (`Backend/database/users.db`) and configuration (`Backend/secrets.json`) are also in `.gitignore` and remain untouched across deployments.

---

## 3. Manual Deployment / Emergency Rollback

If you ever need to manually deploy or roll back to a previous commit on the VPS:

```bash
# 1. Connect to VPS
ssh -i ~/.ssh/toothmanager_deploy stepheng753@69.62.71.85

# 2. Navigate to repo
cd /home/stepheng753/FileStorageApp

# 3. Pull a specific commit or tag (e.g., previous stable commit)
git checkout <commit_hash>

# 4. Activate virtualenv and reinstall if needed
source .venv/bin/activate
pip install -r Backend/requirements.txt

# 5. Restart Gunicorn
sudo systemctl restart gunicorn

# 6. Verify health
curl -k https://dev.toothmanager.com/api/health
```
