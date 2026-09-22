# Tooth Manager - REST API Specification

**Base URL**: `https://dev.toothmanager.com/api` (Production) or `http://localhost:3000/api` (Development)

All authenticated endpoints require an `Authorization` header:
```text
Authorization: Bearer <your_jwt_token>
```

---

## 1. System & Health

### `GET /health`
Returns system status, service name, and version. Used for monitoring and CI/CD validation.

* **Authentication**: None
* **Response (200 OK)**:
```json
{
  "service": "ToothManager API",
  "status": "healthy",
  "timestamp": "2026-09-22T17:50:00.000000",
  "version": "2.0.0"
}
```

---

### `GET /docs`
Interactive Swagger UI documentation page with "Try it out" and Bearer Token authentication testing.

* **URL**: `https://dev.toothmanager.com/docs` or `http://localhost:3000/docs` (also available at `/api/docs`)
* **Authentication**: None (Interactive UI in browser)

---

### `GET /api/openapi.json`
Complete OpenAPI 3.0.3 specification in JSON format.

* **Authentication**: None
* **Response (200 OK)**: OpenAPI 3.0.3 JSON schema


---

## 2. Authentication API (`/auth`)

### `POST /auth/login`
Authenticates user credentials and returns a signed JWT token.

* **Authentication**: None
* **Request Body** (`application/json` or `application/x-www-form-urlencoded`):
```json
{
  "username": "DR_HOANG",
  "password": "SecretPassword123!"
}
```
* **Response (200 OK)**:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "firstname": "Dr.",
    "lastname": "Hoang",
    "username": "DR_HOANG",
    "permission_tier": 1
  }
}
```
* **Error (401 Unauthorized)**:
```json
{
  "success": false,
  "error": "Invalid username or password"
}
```

---

### `POST /auth/register`
Submits a registration request for staff access. Newly created accounts default to Tier 3 (Pending Approval).

* **Authentication**: None
* **Request Body**:
```json
{
  "firstname": "Sarah",
  "lastname": "Connor",
  "username": "sconnor",
  "password": "Password123!"
}
```
* **Response (201 Created)**:
```json
{
  "success": true,
  "message": "Account created successfully. Please wait for an administrator to approve your access.",
  "user": {
    "id": 4,
    "firstname": "Sarah",
    "lastname": "Connor",
    "username": "SCONNOR",
    "permission_tier": 3
  }
}
```

---

### `GET /auth/me`
Fetches the profile and permission tier of the currently authenticated token holder.

* **Authentication**: Bearer Token
* **Response (200 OK)**:
```json
{
  "success": true,
  "user": {
    "id": 1,
    "firstname": "Dr.",
    "lastname": "Hoang",
    "username": "DR_HOANG",
    "permission_tier": 1,
    "created_at": "2025-08-01 12:00:00"
  }
}
```

---

## 3. Documents & Folders API (`/files`)

### `GET /files`
Retrieves directory contents, breadcrumbs, folders, and files for a specified folder path.

* **Authentication**: Tier 1 or Tier 2
* **Query Parameters**:
  - `folder` *(string, optional)*: Relative directory path inside storage (e.g. `401k ADP` or `Consent Forms`). Defaults to root.
  - `view` *(string, optional)*: Set to `tree` to get legacy recursive JSON hierarchy.
* **Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "current_folder": "401k ADP",
    "parent_folder": "",
    "breadcrumbs": [
      { "name": "Home", "path": "" },
      { "name": "401k ADP", "path": "401k ADP" }
    ],
    "folders": [],
    "files": [
      {
        "name": "Manager 401k FAQ.docx",
        "path": "401k ADP/Manager 401k FAQ.docx",
        "is_dir": false,
        "size_bytes": 28412,
        "formatted_size": "27.7 KB",
        "category": "document",
        "modified_at": "2025-12-17T14:32:00"
      },
      {
        "name": "401k Decline Request Form.pdf",
        "path": "401k ADP/401k Decline Request Form.pdf",
        "is_dir": false,
        "size_bytes": 142080,
        "formatted_size": "138.8 KB",
        "category": "pdf",
        "modified_at": "2025-12-17T14:35:12"
      }
    ],
    "total_items": 2
  }
}
```

---

### `POST /files/upload`
Uploads one or multiple files into a practice folder.

* **Authentication**: Tier 1 (Admin)
* **Request Format**: `multipart/form-data`
  - `folder` *(text)*: Destination folder path (e.g. `401k ADP`)
  - `file` *(file or array of files)*: The uploaded file binary payloads
* **Response (201 Created)**:
```json
{
  "success": true,
  "message": "Successfully uploaded 1 file(s)",
  "files": [
    {
      "name": "Policy_Update_2026.pdf",
      "path": "401k ADP/Policy_Update_2026.pdf",
      "size_bytes": 1048576,
      "formatted_size": "1.0 MB",
      "category": "pdf"
    }
  ]
}
```

---

### `POST /files/folder`
Creates a new directory inside storage.

* **Authentication**: Tier 1 (Admin)
* **Request Body**:
```json
{
  "parent_folder": "",
  "folder_name": "Employee Onboarding 2026"
}
```
* **Response (201 Created)**:
```json
{
  "success": true,
  "message": "Folder 'Employee Onboarding 2026' created successfully",
  "folder": {
    "name": "Employee Onboarding 2026",
    "path": "Employee Onboarding 2026",
    "is_dir": true,
    "item_count": 0
  }
}
```

---

### `DELETE /files`
Deletes a specified file or entire folder (recursively).

* **Authentication**: Tier 1 (Admin)
* **Request Body**:
```json
{
  "path": "401k ADP/Old_Document.pdf"
}
```
* **Response (200 OK)**:
```json
{
  "success": true,
  "message": "Successfully deleted '401k ADP/Old_Document.pdf'"
}
```

---

## 4. User Administration API (`/users`)

### `GET /users`
Lists all registered users. Note: Passwords are removed from responses.

* **Authentication**: Tier 1 (Admin)
* **Response (200 OK)**:
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "firstname": "Dr.",
      "lastname": "Hoang",
      "username": "DR_HOANG",
      "permission_tier": 1,
      "created_at": "2025-08-01 12:00:00"
    },
    {
      "id": 2,
      "firstname": "Dental",
      "lastname": "Assistant",
      "username": "ASSISTANT1",
      "permission_tier": 2,
      "created_at": "2025-08-10 09:15:00"
    }
  ]
}
```

---

### `PATCH /users/{username}/tier`
Updates a user's role / permission level.

* **Authentication**: Tier 1 (Admin)
* **Request Body**:
```json
{
  "permission_tier": 2
}
```
* **Response (200 OK)**:
```json
{
  "success": true,
  "message": "Updated permission tier for 'ASSISTANT1' to 2",
  "permission_tier": 2,
  "username": "ASSISTANT1"
}
```

---

### `PATCH /users/{username}/password`
Allows an administrator to reset any user's password.

* **Authentication**: Tier 1 (Admin)
* **Request Body**:
```json
{
  "new_password": "NewSecurePassword123!"
}
```
* **Response (200 OK)**:
```json
{
  "success": true,
  "message": "Password reset successfully for 'ASSISTANT1'"
}
```

---

### `DELETE /users/{username}`
Permanently deletes a user account. Admins cannot delete their own account.

* **Authentication**: Tier 1 (Admin)
* **Response (200 OK)**:
```json
{
  "success": true,
  "message": "User 'ASSISTANT1' deleted successfully"
}
```
