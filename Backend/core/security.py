import datetime
import functools
from flask import request, jsonify
import jwt
from core.config import JWT_SECRET_KEY, JWT_EXPIRES_HOURS

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    import hashlib
    HAS_BCRYPT = False


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt (or sha256 fallback)."""
    if HAS_BCRYPT:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    else:
        # Fallback if bcrypt binary not yet installed in local environment
        salt = "toothmanager_salt"
        return "sha256$" + hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """
    Verify password. Supports:
    1. bcrypt hash (starts with $2a$, $2b$, or $2y$)
    2. sha256 fallback hash (starts with sha256$)
    3. Legacy plaintext password (for backward compatibility during migration)
    """
    if not stored_hash:
        return False

    # Check bcrypt
    if stored_hash.startswith(("$2a$", "$2b$", "$2y$")):
        if HAS_BCRYPT:
            try:
                return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash.encode("utf-8"))
            except Exception:
                return False
        return False

    # Check sha256 fallback
    if stored_hash.startswith("sha256$"):
        salt = "toothmanager_salt"
        expected = "sha256$" + hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
        return expected == stored_hash

    # Check legacy plaintext
    return plain_password == stored_hash


def is_legacy_plaintext(stored_hash: str) -> bool:
    """Returns True if the password is not yet hashed."""
    if not stored_hash:
        return False
    return not (stored_hash.startswith(("$2a$", "$2b$", "$2y$")) or stored_hash.startswith("sha256$"))


def generate_token(user: dict) -> str:
    """Generate a JWT token for the user."""
    payload = {
        "sub": user["username"],
        "user_id": user.get("id"),
        "firstname": user.get("firstname", ""),
        "lastname": user.get("lastname", ""),
        "permission_tier": int(user.get("permission_tier", 3)),
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=JWT_EXPIRES_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])


def get_token_from_request():
    """Extract Bearer token from Authorization header or 'token' query param."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:].strip()
    return request.args.get("token") or request.form.get("token")


def token_required(f):
    """Decorator to require a valid JWT token."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        if not token:
            return jsonify({"success": False, "error": "Authentication token missing"}), 401

        try:
            payload = decode_token(token)
            request.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "error": "Token has expired. Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated


def staff_or_admin_required(f):
    """Decorator to require permission tier 1 (Admin) or 2 (Staff)."""
    @functools.wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        tier = request.current_user.get("permission_tier", 3)
        if tier not in (1, 2):
            return jsonify({
                "success": False,
                "error": "Access denied. Your account is pending administrator approval."
            }), 403
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Decorator to require permission tier 1 (Admin)."""
    @functools.wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        tier = request.current_user.get("permission_tier", 3)
        if tier != 1:
            return jsonify({
                "success": False,
                "error": "Admin privileges required for this action."
            }), 403
        return f(*args, **kwargs)
    return decorated
