#!/usr/bin/env python3
"""
Tooth Manager - Backend Application
Provides RESTful API for authentication, file storage management, and user administration.
"""

from flask import Flask, jsonify, send_from_directory, request, redirect
from flask_cors import CORS
from core.config import (
    SECRET_KEY,
    SERVER_NAME,
    STORAGE_DIR,
    CORS_ORIGINS,
    MAX_CONTENT_LENGTH,
    PORT
)
from database.db import init_db, auto_migrate_plaintext_passwords
from api.health import health_bp
from api.auth import auth_bp
from api.files import files_bp
from api.users import users_bp
from api.docs import docs_bp, get_docs


def create_app() -> Flask:
    app = Flask(__name__, static_folder=str(STORAGE_DIR))

    # App configuration
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    if SERVER_NAME:
        app.config["SERVER_NAME"] = SERVER_NAME

    # Enable CORS
    # Automatically ensure all toothmanager domains (with/without www, http/https) are permitted
    import re
    base_origins = list(CORS_ORIGINS) if isinstance(CORS_ORIGINS, (list, tuple)) else [CORS_ORIGINS]
    extra_origins = [
        "https://toothmanager.com",
        "http://toothmanager.com",
        "https://www.toothmanager.com",
        "http://www.toothmanager.com",
        "https://dev.toothmanager.com",
        "http://dev.toothmanager.com",
        re.compile(r"^https?://([a-zA-Z0-9-]+\.)?toothmanager\.com(:[0-9]+)?$")
    ]
    for o in extra_origins:
        if o not in base_origins and "*" not in base_origins:
            base_origins.append(o)

    CORS(app, origins=base_origins, supports_credentials=True)

    # Initialize Database and check for migrations
    init_db()
    auto_migrate_plaintext_passwords()

    # Register Modern RESTful Blueprints under /api
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(files_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api")
    app.register_blueprint(docs_bp, url_prefix="/api")

    # Swagger Documentation at /docs
    @app.route("/docs", methods=["GET"])
    def serve_swagger_docs():
        return get_docs()

    # Static file serving route (especially useful for local development and Nginx fallback)
    @app.route("/static/<path:filename>")
    def serve_static(filename):
        return send_from_directory(str(STORAGE_DIR), filename)

    # Root index / ping
    @app.route("/", methods=["GET"])
    def root_index():
        return jsonify({
            "service": "Tooth Manager API",
            "version": "2.0.0",
            "status": "online",
            "documentation": "/docs"
        }), 200

    # 404 handler
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "success": False,
            "error": "The requested resource was not found on this server."
        }), 404

    # 413 handler (payload too large)
    @app.errorhandler(413)
    def request_entity_too_large(e):
        return jsonify({
            "success": False,
            "error": "File size exceeds the 1 GB maximum upload limit."
        }), 413

    # 500 handler
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            "success": False,
            "error": "An internal server error occurred."
        }), 500

    # --- Legacy Endpoint Compatibility Shims ---
    from api.auth import login as api_login, register as api_register
    from api.files import list_files as api_list_files, upload_files as api_upload_files, remove_item as api_remove_item
    from api.users import list_all_users as api_list_all_users

    @app.route("/login", methods=["POST"])
    def legacy_login():
        return api_login()

    @app.route("/register", methods=["POST"])
    def legacy_register():
        return api_register()

    @app.route("/download_files", methods=["GET", "POST"])
    def legacy_download_files():
        from core.storage import get_full_folder_tree
        return jsonify(get_full_folder_tree())

    @app.route("/upload_file", methods=["POST"])
    def legacy_upload():
        return api_upload_files()

    @app.route("/delete_file", methods=["POST"])
    def legacy_delete():
        return api_remove_item()

    @app.route("/get_all_users", methods=["GET"])
    def legacy_users():
        return api_list_all_users()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
