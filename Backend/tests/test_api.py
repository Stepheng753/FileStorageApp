import pytest
from app import create_app
from database.db import create_user
from core.security import hash_password, generate_token


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.0.0"


def test_swagger_docs(client):
    res = client.get("/docs")
    assert res.status_code == 200
    assert b"SwaggerUIBundle" in res.data
    assert b"Tooth Manager API Documentation" in res.data

    # Also check /api/docs
    res_api = client.get("/api/docs")
    assert res_api.status_code == 200


def test_openapi_spec(client):
    res = client.get("/api/openapi.json")
    assert res.status_code == 200
    data = res.get_json()
    assert data["openapi"] == "3.0.3"
    assert "/api/files" in data["paths"]
    assert "/api/auth/login" in data["paths"]


def test_auth_flow(client):
    # Register a new user
    res = client.post("/api/auth/register", json={
        "firstname": "Test",
        "lastname": "User",
        "username": "testuser_api",
        "password": "Password123!"
    })
    # If already created or 201
    assert res.status_code in (201, 409)

    # Login
    login_res = client.post("/api/auth/login", json={
        "username": "testuser_api",
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    login_data = login_res.get_json()
    assert login_data["success"] is True
    assert "token" in login_data
    token = login_data["token"]

    # Access /api/auth/me with Bearer token
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.get_json()
    assert me_data["user"]["username"] == "TESTUSER_API"


def test_unauthorized_access(client):
    res = client.get("/api/files")
    assert res.status_code == 401
