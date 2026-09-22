from datetime import datetime
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Uptime health check endpoint for monitoring and CI/CD validation."""
    return jsonify({
        "status": "healthy",
        "service": "ToothManager API",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }), 200
