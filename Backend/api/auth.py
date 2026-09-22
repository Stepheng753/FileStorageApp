from flask import Blueprint, request, jsonify
from core.security import (
    hash_password,
    verify_password,
    is_legacy_plaintext,
    generate_token,
    token_required
)
from database.db import (
    get_user_by_username,
    create_user,
    update_user_password
)

auth_bp = Blueprint("auth", __name__)


def get_request_data():
    """Helper to extract data whether sent as JSON or multipart/form-data."""
    if request.is_json:
        return request.get_json() or {}
    return request.form.to_dict() if request.form else {}


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user with username and password, return JWT token."""
    data = get_request_data()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"success": False, "error": "Username and password are required"}), 400

    user = get_user_by_username(username)
    if not user:
        return jsonify({"success": False, "error": "Invalid username or password"}), 401

    stored_pass = user.get("password", "")
    if not verify_password(password, stored_pass):
        return jsonify({"success": False, "error": "Invalid username or password"}), 401

    # Transparently upgrade plain text password if needed
    if is_legacy_plaintext(stored_pass):
        new_hash = hash_password(password)
        update_user_password(user["username"], new_hash)

    token = generate_token(user)
    return jsonify({
        "success": True,
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "firstname": user.get("firstname", ""),
            "lastname": user.get("lastname", ""),
            "permission_tier": int(user.get("permission_tier", 3))
        }
    }), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user account (starts with Tier 3: Pending Approval)."""
    data = get_request_data()
    firstname = data.get("firstname", "").strip()
    lastname = data.get("lastname", "").strip()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not all([firstname, lastname, username, password]):
        return jsonify({"success": False, "error": "All fields are required (firstname, lastname, username, password)"}), 400

    if len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters long"}), 400

    existing = get_user_by_username(username)
    if existing:
        return jsonify({"success": False, "error": "Username already taken. Please choose another."}), 409

    pwd_hash = hash_password(password)
    user = create_user(
        firstname=firstname,
        lastname=lastname,
        username=username,
        password_hash=pwd_hash,
        permission_tier=3  # Default tier 3: pending administrator approval
    )

    if not user:
        return jsonify({"success": False, "error": "Failed to create user account"}), 500

    return jsonify({
        "success": True,
        "message": "Account created successfully. Please wait for an administrator to approve your access.",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "firstname": user["firstname"],
            "lastname": user["lastname"],
            "permission_tier": user["permission_tier"]
        }
    }), 201


@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user():
    """Get the current authenticated user's profile and active permissions."""
    username = request.current_user.get("sub")
    user = get_user_by_username(username)
    if not user:
        return jsonify({"success": False, "error": "User no longer exists"}), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "firstname": user.get("firstname", ""),
            "lastname": user.get("lastname", ""),
            "permission_tier": int(user.get("permission_tier", 3)),
            "created_at": user.get("created_at")
        }
    }), 200


@auth_bp.route("/change-password", methods=["POST"])
@token_required
def change_password():
    """Change the authenticated user's password."""
    data = get_request_data()
    old_password = data.get("old_password", "")
    new_password = data.get("new_password", "")

    if not old_password or not new_password:
        return jsonify({"success": False, "error": "Both old and new passwords are required"}), 400

    if len(new_password) < 6:
        return jsonify({"success": False, "error": "New password must be at least 6 characters long"}), 400

    username = request.current_user.get("sub")
    user = get_user_by_username(username)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    if not verify_password(old_password, user.get("password", "")):
        return jsonify({"success": False, "error": "Current password incorrect"}), 400

    new_hash = hash_password(new_password)
    success = update_user_password(username, new_hash)
    if not success:
        return jsonify({"success": False, "error": "Failed to update password"}), 500

    return jsonify({"success": True, "message": "Password updated successfully"}), 200
