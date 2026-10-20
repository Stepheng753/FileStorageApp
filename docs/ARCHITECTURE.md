# Tooth Manager - Architecture & Storage Guide

## System Overview

Tooth Manager is a dental practice document management system designed to provide secure, role-based access to practice documents, administrative files, patient forms, and human resource policies.

The system consists of:
1. **Frontend**: Standalone responsive web client styled with a custom dental theme (Milky Way typography, pastel color palette, glassmorphism, responsive CSS grid).
2. **Backend**: Python Flask RESTful API structured with modular blueprints (`auth`, `files`, `users`, `health`).
3. **Database**: SQLite3 database (`Backend/database/users.db`) with dictionary rows, indexed lookups, and automatic password hash migrations.
4. **Storage Layer**: Server filesystem storage (`Backend/static/`) configured via `secrets.json`. It is never served directly over HTTP; every read goes through the authenticated files API.

```mermaid
graph TD
    Client["Browser / Client (Desktop & Mobile)"] -->|HTTPS :443| Nginx["Nginx Reverse Proxy (dev.toothmanager.com)"]
    Nginx -->|Proxy /api/* to Unix Socket| Gunicorn["Gunicorn WSGI Server (/tmp/gunicorn.sock)"]
    Gunicorn --> FlaskApp["Flask Application (Backend/app.py)"]
    FlaskApp --> AuthModule["Auth API (/api/auth)"]
    FlaskApp --> FilesModule["Files API (/api/files)"]
    FlaskApp --> UsersModule["Users API (/api/users)"]
    FlaskApp --> HealthModule["Health API (/api/health)"]
    FilesModule --> StorageCore["Storage Layer (Path Confinement, Extension & Content Checks)"]
    StorageCore --> StaticFS["Local Storage: Backend/static/ (not served over HTTP)"]
    AuthModule --> DBCore["Database Layer (db.py)"]
    UsersModule --> DBCore
    DBCore --> SQLite[("SQLite: Backend/database/users.db")]
```

---

## 1. Where Are the Files Saved?

### File System Path
All documents and practice folders reside on the server filesystem at:
```text
/home/stepheng753/FileStorageApp/Backend/static/
```

In the backend codebase, this path is controlled by `Backend/core/config.py`:
- `STORAGE_DIR`: defaults to `static` (relative to the `Backend` directory) or configured via `"STORAGE_DIR"` in `Backend/secrets.json`.

### Directory Structure & Production Content
Folders in the static directory represent practice categories, such as:
- `Backend/static/401k ADP/`
- `Backend/static/CareCredit/`
- `Backend/static/Consent Forms/`
- `Backend/static/Dental Assistants/`
- `Backend/static/Dr. Hoang Licenses/`
- `Backend/static/Human Resources/`
- `Backend/static/Insurance/`
- `Backend/static/OSHA/`
- ...and 40+ additional practice folders.

### File Access
- **No static file route.** Flask is created without a `static_folder`, and Nginx has no `/static/` location. Nothing in `Backend/static/` is reachable by URL.
- **Viewing and downloading**: the frontend calls `GET /api/files/download?path=...` with the Bearer token and opens the result from a blob URL. Plain links cannot send the token, so they are not used.

### Security & Directory Traversal Protection
In legacy versions, uploading or deleting files could be exploited via relative paths (`../../`). The current implementation is in `Backend/core/storage.py`:
1. `clean_relative_path()` removes null bytes, leading slashes, and `.`/`..` segments from every user-supplied path. Names are otherwise left exactly as supplied.
2. `resolve_safe_path()` resolves canonical filesystem paths using `pathlib.Path.resolve()` and verifies that `os.path.commonpath([target, storage_root]) == storage_root`. This also rejects symlinks that point outside storage.
3. `validate_upload_filename()` keeps the original name, including spaces and Unicode. It only trims directory parts. It rejects dotfiles, executable and script extensions (checked across every dot-separated suffix), and any extension outside the allowlist: `pdf, docx, doc, xlsx, xls, pptx, ppt, png, jpg, jpeg, txt, csv`.
4. `validate_upload_content()` checks magic bytes against the extension (PDF, PNG, JPEG, ZIP-based OOXML, OLE2 legacy Office). Text files must not contain NUL bytes.
5. Uploaded files are written with mode `0644`. Directories created by a request are `0755`.
6. Upload, folder creation, and delete require a Tier 1 token. The token is read from the `Authorization` header or the `token` query parameter. The form body is not read for tokens, so unauthenticated uploads are rejected without buffering the payload.

---

## 2. Security & Authentication Architecture

### Authentication Flow (JWT)
1. **Log In**: Client sends credentials (`POST /api/auth/login`).
2. **Verification**: Backend checks password against bcrypt hash. If a legacy plaintext password is encountered, it is automatically migrated to bcrypt.
3. **Token Issuance**: Backend generates a signed JSON Web Token (JWT) using HS256 and `JWT_SECRET_KEY` from `secrets.json`, containing:
   - `sub`: username
   - `user_id`: database primary key
   - `permission_tier`: 1 (Admin), 2 (Staff), or 3 (Pending)
   - `exp`: expiration (24 hours by default)
4. **Authorized Requests**: Client sends `Authorization: Bearer <token>` on all requests.

### Role-Based Access Control (RBAC)

| Tier | Role | Capabilities |
| :--- | :--- | :--- |
| **Tier 1** | **Administrator** (e.g. Dr. Hoang) | • Full document access (Browse, View, Download)<br>• Upload new documents<br>• Create new folders<br>• Delete files and folders<br>• View all user accounts<br>• Approve pending registrations (Change Tier)<br>• Reset user passwords<br>• Delete user accounts |
| **Tier 2** | **Staff Member** | • Browse practice folders<br>• Search documents<br>• View and download files<br>• Cannot upload, delete, or manage users |
| **Tier 3** | **Pending Approval** | • Newly registered accounts<br>• Cannot access any documents or patient files<br>• Displays pending authorization notice |

---

## 3. Database Schema

The database is managed by SQLite3 at `Backend/database/users.db`:

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,                -- bcrypt hash ($2b$12$...)
    permission_tier INTEGER NOT NULL DEFAULT 3, -- 1=Admin, 2=Staff, 3=Pending
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
```
