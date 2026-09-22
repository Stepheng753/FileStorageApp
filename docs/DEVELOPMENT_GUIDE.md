# Tooth Manager - Local Development Guide

This guide describes how to run and test Tooth Manager locally under WSL or Linux.

---

## 1. Prerequisites

- Python 3.10 or higher
- `pip` and `virtualenv` / `venv`
- Modern web browser (Chrome, Firefox, Edge, Safari)

---

## ⚡ Quick System Control (`scripts/system.sh`)

Tooth Manager provides a unified CLI helper script [`scripts/system.sh`](file:///home/stepheng753/Development/FileStorageApp/scripts/system.sh) to start, stop, restart, and monitor services with automatic PID tracking and log management:

```bash
# Start Backend API (:3000) and Frontend (:8080)
./scripts/system.sh --start

# Check service status and health check ping
./scripts/system.sh --status

# Follow live backend logs
./scripts/system.sh --logs backend

# Follow live frontend logs
./scripts/system.sh --logs frontend

# Stop all running services
./scripts/system.sh --stop

# Restart all services
./scripts/system.sh --restart

# Run pytest automated test suite
./scripts/system.sh --test

# Display help menu
./scripts/system.sh --help
```

---


## 2. Setting Up the Local Environment

### Step 1: Clone and Navigate to the Repository
```bash
git clone https://github.com/Stepheng753/FileStorageApp.git
cd FileStorageApp
```

### Step 2: Create and Activate Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r Backend/requirements.txt
```

### Step 4: Configure Local `secrets.json`
Copy the example configuration:
```bash
cp Backend/secrets.example.json Backend/secrets.json
```
For local development, `SERVER_NAME` is set to `null` so Flask allows requests from `localhost` and `127.0.0.1`.

---

## 3. Creating an Admin Account

Run the database setup script to create an initial administrator account:
```bash
python3 -c "
from Backend.database.db import init_db, create_user
from Backend.core.security import hash_password

init_db()
user = create_user(
    firstname='Dr.',
    lastname='Hoang',
    username='DR_HOANG',
    password_hash=hash_password('AdminPassword123!'),
    permission_tier=1
)
print('Admin user ready:', user)
"
```

---

## 4. Running the Development Server

Start the Flask backend API:
```bash
cd Backend
python3 app.py
```
The API will run at `http://127.0.0.1:3000`.

To verify it is running, open another terminal or browser:
```bash
curl http://127.0.0.1:3000/api/health
```

---

## 5. Running the Frontend

Because the frontend is built with pure vanilla HTML, modern CSS, and ES JavaScript, you can run it using any lightweight HTTP server or VS Code Live Server:

```bash
# Using Python's built-in HTTP server:
cd Frontend
python3 -m http.server 8080
```
Then visit:
```text
http://127.0.0.1:8080/index.html
```

Or open `Frontend/index.html` directly in your web browser.

---

## 6. Running the Test Suite

Run automated unit and integration tests using `pytest`:
```bash
cd Backend
pytest -v tests/
```
The test suite validates:
- Password hashing and legacy hash migration
- JWT token encoding and decoding
- Path boundary containment (directory traversal prevention)
- Directory browsing and formatting helpers
- Full authentication and registration workflow
