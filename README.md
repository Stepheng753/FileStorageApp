# 🦷 Tooth Manager

[![CI/CD Pipeline](https://github.com/Stepheng753/FileStorageApp/actions/workflows/deploy.yml/badge.svg)](https://github.com/Stepheng753/FileStorageApp/actions/workflows/deploy.yml)
[![REST API](https://img.shields.io/badge/API-RESTful%20v2.0-8FD0C6)](https://dev.toothmanager.com/docs)
[![Swagger Docs](https://img.shields.io/badge/Swagger-OpenAPI%203.0-green.svg)](https://dev.toothmanager.com/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-EEDDCF.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

**Tooth Manager** is a modern document management and file portal designed specifically for dental practices. It provides secure, role-based access to practice documents, human resource policies, patient forms, and compliance licenses.

---

## ⚡ Quick System Control (`scripts/system.sh`)

Manage and run all local services with a single unified script:

```bash
# Start both Backend API (:3000) and Frontend (:8080)
./scripts/system.sh --start

# Check live service status and API health ping
./scripts/system.sh --status

# Stop all running Tooth Manager services
./scripts/system.sh --stop

# Restart all services
./scripts/system.sh --restart

# Follow live backend logs
./scripts/system.sh --logs backend

# Run the automated Pytest test suite
./scripts/system.sh --test

# Display help and all available commands
./scripts/system.sh --help
```

---

## 📖 Complete Documentation Suite

All system details, architecture breakdowns, and deployment steps are documented in dedicated guides:

| Document | Purpose & Contents |
| :--- | :--- |
| 🏗️ [**Architecture & Storage Guide**](file:///home/stepheng753/Development/FileStorageApp/docs/ARCHITECTURE.md) | Component architecture (Mermaid), exact storage filesystem paths, path boundary security, and SQLite schema. |
| ⚡ [**Interactive Swagger UI**](https://dev.toothmanager.com/docs) | Live Swagger documentation page with "Try It Out" and Bearer Token authentication (`/docs` or `/api/docs`). |
| 📜 [**REST API Specification**](file:///home/stepheng753/Development/FileStorageApp/docs/API_SPECIFICATION.md) | Full endpoint reference, JSON schemas, headers, status codes, and cURL examples. |
| 🚀 [**Production VPS Deployment Guide**](file:///home/stepheng753/Development/FileStorageApp/docs/DEPLOYMENT_GUIDE.md) | VPS specs (`69.62.71.85`), Nginx reverse proxy, Certbot SSL, systemd Gunicorn service, and permissions. |
| 🔄 [**CI/CD Pipeline & SSH Setup**](file:///home/stepheng753/Development/FileStorageApp/docs/CICD_PIPELINE.md) | Step-by-step SSH key generation, GitHub Secrets configuration, automated deployment workflow, and rollback. |
| 💻 [**Local Development Guide**](file:///home/stepheng753/Development/FileStorageApp/docs/DEVELOPMENT_GUIDE.md) | Running locally with WSL/Linux, virtual environment setup, configuration, and running the test suite. |

---

## 📁 Where Are the Files Saved?

All uploaded documents and practice folders reside on the server filesystem at:
```text
/home/stepheng753/FileStorageApp/Backend/static/
```

- **Storage Location**: Controlled via `STORAGE_DIR` in `Backend/core/config.py` (configured in `Backend/secrets.json`).
- **High Performance Delivery**: In production, Nginx serves `/static/` directly from disk with caching and zero Gunicorn overhead.
- **Data Protection**: In `.gitignore`, `Backend/static/*` is strictly ignored to ensure deployments **never overwrite or delete existing client documents**.
- **Path Traversal Guards**: Filenames are sanitized with `secure_filename`, and directory paths are validated against `STORAGE_DIR` boundaries to prevent traversal attacks (`../../`).

---

## 🔒 Security & Role-Based Access Control (RBAC)

Tooth Manager protects practice documents through industry-standard **bcrypt** password hashing and **JWT** session authentication:

| Tier | Role | Access Level |
| :--- | :--- | :--- |
| **Tier 1** | **Administrator** *(e.g. Dr. Hoang)* | Full permissions: view, download, upload files, create folders, batch delete, approve registrations, change roles, reset passwords. |
| **Tier 2** | **Practice Staff** | View & download practice documents and forms. Cannot upload, delete, or manage users. |
| **Tier 3** | **Pending Approval** | Newly registered accounts. Placed in pending status until approved by an administrator. |

---

## 🌐 Endpoints & Interactive Swagger Page

The API includes built-in interactive Swagger documentation:

- **Swagger Documentation**: [http://localhost:3000/docs](http://localhost:3000/docs) (or [https://dev.toothmanager.com/docs](https://dev.toothmanager.com/docs))
- **OpenAPI 3.0.3 Spec**: `GET /api/openapi.json`
- **Uptime Health Ping**: `GET /api/health`

---

## 🚀 Manual Local Development Setup

If you prefer to run services manually instead of using `./scripts/system.sh`:

### 1. Backend Setup
```bash
# Clone repository
git clone https://github.com/Stepheng753/FileStorageApp.git
cd FileStorageApp/Backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create secrets configuration
cp secrets.example.json secrets.json

# Start development API server (runs on port 3000)
python3 app.py
```

### 2. Frontend Access
Open `Frontend/index.html` in your web browser or run a lightweight local server:
```bash
cd ../Frontend
python3 -m http.server 8080
```
Then visit `http://localhost:8080/index.html`.

---

## 🔄 GitHub Actions CI/CD to Production VPS

When code is pushed to `main`, `.github/workflows/deploy.yml` automatically:
1. Runs the test suite via `pytest`.
2. Connects via SSH to `stepheng753@69.62.71.85`.
3. Pulls latest release updates while **preserving all uploaded static files and the SQLite database**.
4. Installs updated dependencies in `.venv`.
5. Gracefully reloads the Gunicorn service (`sudo systemctl restart gunicorn`).
6. Verifies system health via `/api/health`.

For setup instructions on SSH keys and GitHub Secrets, see [docs/CICD_PIPELINE.md](file:///home/stepheng753/Development/FileStorageApp/docs/CICD_PIPELINE.md).
