from flask import Blueprint, request, jsonify
from core.security import admin_required, hash_password
from database.db import (
    get_all_users,
    get_user_by_username,
    update_user_permission,
    update_user_password,
    delete_user_by_username
)

users_bp = Blueprint("users", __name__)


def get_request_data():
    if request.is_json:
        return request.get_json() or {}
    return request.form.to_dict() if request.form else {}


@users_bp.route("/users", methods=["GET"])
@admin_required
def list_all_users():
    """Retrieve all users without password hashes (Admin only)."""
    users = get_all_users(include_passwords=False)
    return jsonify({"success": True, "users": users}), 200


@users_bp.route("/users/<username>", methods=["GET"])
@admin_required
def get_user_detail(username: str):
    """Retrieve details for a specific user (Admin only)."""
    user = get_user_by_username(username)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    # Remove password from response
    user_data = {
        "id": user["id"],
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "username": user["username"],
        "permission_tier": user["permission_tier"],
        "created_at": user.get("created_at")
    }
    return jsonify({"success": True, "user": user_data}), 200


@users_bp.route("/users/<username>/tier", methods=["PATCH", "POST"])
@admin_required
def update_tier(username: str):
    """Update a user's permission tier (Admin only)."""
    data = get_request_data()
    tier = data.get("permission_tier")
    if tier is None:
        return jsonify({"success": False, "error": "permission_tier is required"}), 400

    try:
        tier_int = int(tier)
        if tier_int not in (1, 2, 3):
            return jsonify({"success": False, "error": "Permission tier must be 1 (Admin), 2 (Staff), or 3 (Pending)"}), 400
    except ValueError:
        return jsonify({"success": False, "error": "Invalid permission tier number"}), 400

    user = get_user_by_username(username)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    success = update_user_permission(username, tier_int)
    if not success:
        return jsonify({"success": False, "error": "Failed to update permission tier"}), 500

    return jsonify({
        "success": True,
        "message": f"Updated permission tier for '{username}' to {tier_int}",
        "username": username,
        "permission_tier": tier_int
    }), 200


@users_bp.route("/users/<username>/password", methods=["PATCH", "POST"])
@admin_required
def reset_password(username: str):
    """Reset a user's password (Admin override)."""
    data = get_request_data()
    new_password = data.get("new_password", "")
    if not new_password or len(new_password) < 6:
        return jsonify({"success": False, "error": "New password must be at least 6 characters"}), 400

    user = get_user_by_username(username)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    new_hash = hash_password(new_password)
    success = update_user_password(username, new_hash)
    if not success:
        return jsonify({"success": False, "error": "Failed to update password"}), 500

    return jsonify({"success": True, "message": f"Password reset successfully for '{username}'"}), 200


@users_bp.route("/users/<username>", methods=["DELETE"])
@admin_required
def delete_user(username: str):
    """Delete a user account (Admin only)."""
    current_username = request.current_user.get("sub", "").upper()
    if username.strip().upper() == current_username:
        return jsonify({"success": False, "error": "You cannot delete your own account"}), 400

    user = get_user_by_username(username)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    success = delete_user_by_username(username)
    if not success:
        return jsonify({"success": False, "error": "Failed to delete user"}), 500

    return jsonify({"success": True, "message": f"User '{username}' deleted successfully"}), 200
