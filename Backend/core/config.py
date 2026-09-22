import os
import json
from pathlib import Path

# Base directory for the Backend application
BACKEND_DIR = Path(__file__).resolve().parent.parent

# Load configuration from secrets.json (or fallback to defaults)
SECRETS_FILE = BACKEND_DIR / "secrets.json"
EXAMPLE_FILE = BACKEND_DIR / "secrets.example.json"

config_data = {}
if SECRETS_FILE.exists():
    try:
        with open(SECRETS_FILE, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as e:
        print(f"[CONFIG WARNING] Could not parse {SECRETS_FILE}: {e}")
elif EXAMPLE_FILE.exists():
    try:
        with open(EXAMPLE_FILE, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception:
        pass

SECRET_KEY = config_data.get("SECRET_KEY", "fallback-secret-key-replace-in-production")
JWT_SECRET_KEY = config_data.get("JWT_SECRET_KEY", "fallback-jwt-key-replace-in-production")
JWT_EXPIRES_HOURS = int(config_data.get("JWT_EXPIRES_HOURS", 24))
SERVER_NAME = config_data.get("SERVER_NAME", None)
PORT = int(config_data.get("PORT", 3000))
CORS_ORIGINS = config_data.get("CORS_ORIGINS", ["*"])

# Database Path (resolve relative paths against BACKEND_DIR)
db_setting = config_data.get("DATABASE_PATH", "database/users.db")
if os.path.isabs(db_setting):
    DB_PATH = Path(db_setting)
else:
    DB_PATH = (BACKEND_DIR / db_setting).resolve()

# Storage Directory for uploaded files (resolve relative paths against BACKEND_DIR)
storage_setting = config_data.get("STORAGE_DIR", "static")
if os.path.isabs(storage_setting):
    STORAGE_DIR = Path(storage_setting)
else:
    STORAGE_DIR = (BACKEND_DIR / storage_setting).resolve()

# Ensure directories exist
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# 1 GB file upload limit
MAX_CONTENT_LENGTH = 1 * 1024 * 1024 * 1024
