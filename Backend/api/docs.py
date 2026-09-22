from flask import Blueprint, jsonify, render_template_string

docs_bp = Blueprint("docs", __name__)

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Tooth Manager REST API",
        "description": "API for Tooth Manager dental document storage, practice file management, and staff access control.",
        "version": "2.0.0",
        "contact": {
            "name": "Tooth Manager Practice Support",
            "url": "https://dev.toothmanager.com"
        }
    },
    "servers": [
        {"url": "/", "description": "Current Environment Server"},
        {"url": "https://dev.toothmanager.com", "description": "Production VPS"},
        {"url": "http://localhost:3000", "description": "Local Development Server"}
    ],
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter the JWT token obtained from POST /api/auth/login"
            }
        },
        "schemas": {
            "StandardSuccess": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": True},
                    "message": {"type": "string", "example": "Operation completed successfully"}
                }
            },
            "StandardError": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": False},
                    "error": {"type": "string", "example": "Detailed error message"}
                }
            },
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "firstname": {"type": "string", "example": "Dr."},
                    "lastname": {"type": "string", "example": "Hoang"},
                    "username": {"type": "string", "example": "DR_HOANG"},
                    "permission_tier": {"type": "integer", "example": 1, "description": "1: Admin, 2: Staff, 3: Pending"},
                    "created_at": {"type": "string", "example": "2026-01-01 12:00:00"}
                }
            },
            "FileItem": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Policy_Update.pdf"},
                    "path": {"type": "string", "example": "401k ADP/Policy_Update.pdf"},
                    "is_dir": {"type": "boolean", "example": False},
                    "size_bytes": {"type": "integer", "example": 142080},
                    "formatted_size": {"type": "string", "example": "138.8 KB"},
                    "category": {"type": "string", "example": "pdf"},
                    "modified_at": {"type": "string", "example": "2026-03-12T14:32:00"}
                }
            },
            "FolderItem": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "401k ADP"},
                    "path": {"type": "string", "example": "401k ADP"},
                    "is_dir": {"type": "boolean", "example": True},
                    "item_count": {"type": "integer", "example": 12},
                    "modified_at": {"type": "string", "example": "2026-03-12T14:32:00"}
                }
            }
        }
    },
    "paths": {
        "/api/health": {
            "get": {
                "summary": "Health Check & System Status",
                "tags": ["System"],
                "responses": {
                    "200": {
                        "description": "System is healthy",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "healthy"},
                                        "service": {"type": "string", "example": "ToothManager API"},
                                        "version": {"type": "string", "example": "2.0.0"},
                                        "timestamp": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/auth/login": {
            "post": {
                "summary": "Log In with Username and Password",
                "tags": ["Authentication"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["username", "password"],
                                "properties": {
                                    "username": {"type": "string", "example": "DR_HOANG"},
                                    "password": {"type": "string", "example": "AdminPass123!"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login successful, returns JWT token",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "token": {"type": "string", "example": "eyJhbGciOiJIUzI1Ni..."},
                                        "user": {"$ref": "#/components/schemas/User"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Invalid credentials", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/StandardError"}}}}
                }
            }
        },
        "/api/auth/register": {
            "post": {
                "summary": "Request Staff Account",
                "tags": ["Authentication"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["firstname", "lastname", "username", "password"],
                                "properties": {
                                    "firstname": {"type": "string", "example": "Jane"},
                                    "lastname": {"type": "string", "example": "Doe"},
                                    "username": {"type": "string", "example": "jdoe"},
                                    "password": {"type": "string", "example": "SecurePass123!"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "Account created pending approval", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/StandardSuccess"}}}},
                    "409": {"description": "Username already taken", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/StandardError"}}}}
                }
            }
        },
        "/api/auth/me": {
            "get": {
                "summary": "Get Profile for Current Token",
                "tags": ["Authentication"],
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Current user profile",
                        "content": {"application/json": {"schema": {"type": "object", "properties": {"success": {"type": "boolean"}, "user": {"$ref": "#/components/schemas/User"}}}}}
                    },
                    "401": {"description": "Token expired or missing"}
                }
            }
        },
        "/api/auth/change-password": {
            "post": {
                "summary": "Change Current User Password",
                "tags": ["Authentication"],
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["old_password", "new_password"],
                                "properties": {
                                    "old_password": {"type": "string"},
                                    "new_password": {"type": "string", "minLength": 6}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Password updated successfully"},
                    "400": {"description": "Invalid password"}
                }
            }
        },
        "/api/files": {
            "get": {
                "summary": "Browse Directory Contents & Breadcrumbs",
                "tags": ["Documents & Folders"],
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "folder",
                        "in": "query",
                        "description": "Relative directory path (e.g. '401k ADP')",
                        "schema": {"type": "string", "example": ""}
                    },
                    {
                        "name": "view",
                        "in": "query",
                        "description": "Set to 'tree' for legacy recursive tree",
                        "schema": {"type": "string", "example": ""}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Directory items and breadcrumbs",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "current_folder": {"type": "string"},
                                                "parent_folder": {"type": "string"},
                                                "breadcrumbs": {"type": "array", "items": {"type": "object"}},
                                                "folders": {"type": "array", "items": {"$ref": "#/components/schemas/FolderItem"}},
                                                "files": {"type": "array", "items": {"$ref": "#/components/schemas/FileItem"}},
                                                "total_items": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "delete": {
                "summary": "Delete File or Folder (Admin Only)",
                "tags": ["Documents & Folders"],
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["path"],
                                "properties": {
                                    "path": {"type": "string", "example": "401k ADP/Old_Document.pdf"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Item deleted"},
                    "403": {"description": "Admin privileges required"},
                    "404": {"description": "File or folder not found"}
                }
            }
        },
        "/api/files/upload": {
            "post": {
                "summary": "Upload Files to Folder (Admin Only)",
                "tags": ["Documents & Folders"],
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "required": ["folder", "file"],
                                "properties": {
                                    "folder": {"type": "string", "example": "401k ADP"},
                                    "file": {"type": "string", "format": "binary", "description": "File or files to upload"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "Files uploaded successfully"},
                    "403": {"description": "Admin privileges required"}
                }
            }
        },
        "/api/files/folder": {
            "post": {
                "summary": "Create New Folder (Admin Only)",
                "tags": ["Documents & Folders"],
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["folder_name"],
                                "properties": {
                                    "parent_folder": {"type": "string", "example": ""},
                                    "folder_name": {"type": "string", "example": "Consent Forms 2026"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "Folder created successfully"},
                    "403": {"description": "Admin privileges required"}
                }
            }
        },
        "/api/files/download": {
            "get": {
                "summary": "Download or Stream Document (Staff or Admin)",
                "tags": ["Documents & Folders"],
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "path",
                        "in": "query",
                        "required": True,
                        "description": "Relative file path (e.g. '401k ADP/faq.pdf')",
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "download",
                        "in": "query",
                        "description": "'true' to force download attachment, 'false' for in-browser view",
                        "schema": {"type": "boolean", "default": False}
                    }
                ],
                "responses": {
                    "200": {"description": "File binary stream"},
                    "404": {"description": "File not found"}
                }
            }
        },
        "/api/users": {
            "get": {
                "summary": "List All Registered Users (Admin Only)",
                "tags": ["User Administration"],
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "List of user accounts without passwords",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "users": {"type": "array", "items": {"$ref": "#/components/schemas/User"}}
                                    }
                                }
                            }
                        }
                    },
                    "403": {"description": "Admin privileges required"}
                }
            }
        },
        "/api/users/{username}/tier": {
            "patch": {
                "summary": "Update User Permission Tier (Admin Only)",
                "tags": ["User Administration"],
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "username", "in": "path", "required": True, "schema": {"type": "string"}}
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["permission_tier"],
                                "properties": {
                                    "permission_tier": {"type": "integer", "enum": [1, 2, 3], "example": 2}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Role updated"},
                    "404": {"description": "User not found"}
                }
            }
        },
        "/api/users/{username}/password": {
            "patch": {
                "summary": "Reset User Password (Admin Only)",
                "tags": ["User Administration"],
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "username", "in": "path", "required": True, "schema": {"type": "string"}}
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["new_password"],
                                "properties": {
                                    "new_password": {"type": "string", "minLength": 6, "example": "NewPass123!"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Password updated"},
                    "404": {"description": "User not found"}
                }
            }
        },
        "/api/users/{username}": {
            "delete": {
                "summary": "Delete User Account (Admin Only)",
                "tags": ["User Administration"],
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "username", "in": "path", "required": True, "schema": {"type": "string"}}
                ],
                "responses": {
                    "200": {"description": "User deleted successfully"},
                    "400": {"description": "Cannot delete own account"},
                    "404": {"description": "User not found"}
                }
            }
        }
    }
}

SWAGGER_UI_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tooth Manager - Swagger API Docs</title>
  <link rel="icon" href="/static/tooth.png" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
  <style>
    body {
      margin: 0;
      background: #f8faf9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .topbar {
      display: none !important;
    }
    .custom-header {
      background-color: #eedfd5;
      padding: 1rem 2rem;
      border-bottom: 2px solid #8fd0c6;
      box-shadow: 0 2px 10px rgba(0,0,0,0.05);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .custom-title {
      font-size: 1.8rem;
      color: #213230;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .swagger-ui .btn.authorize {
      background-color: #8fd0c6;
      border-color: #8fd0c6;
      color: #213230;
    }
    .swagger-ui .btn.authorize svg {
      fill: #213230;
    }
  </style>
</head>
<body>
  <div class="custom-header">
    <div class="custom-title">
      <span>🦷</span> Tooth Manager API Documentation
    </div>
    <div>
      <a href="/" style="text-decoration: none; font-weight: 600; color: #213230; background: rgba(255,255,255,0.7); padding: 0.4rem 0.9rem; border-radius: 6px;">Return to App ➔</a>
    </div>
  </div>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
  <script>
    window.onload = () => {
      window.ui = SwaggerUIBundle({
        url: '/api/openapi.json',
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>
"""


@docs_bp.route("/openapi.json", methods=["GET"])
def get_openapi_spec():
    """Serve the OpenAPI 3.0 specification as JSON."""
    return jsonify(OPENAPI_SPEC)


@docs_bp.route("/docs", methods=["GET"])
def get_docs():
    """Serve interactive Swagger UI documentation page."""
    return render_template_string(SWAGGER_UI_HTML)
