import pytest
from core.security import (
    hash_password,
    verify_password,
    is_legacy_plaintext,
    generate_token,
    decode_token
)


def test_password_hashing():
    pwd = "ToothSecretPassword123!"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_legacy_plaintext_detection():
    assert is_legacy_plaintext("plain_text_123") is True
    hashed = hash_password("secret")
    assert is_legacy_plaintext(hashed) is False


def test_jwt_token_generation_and_decoding():
    user = {
        "id": 1,
        "username": "DR_HOANG",
        "firstname": "Dr.",
        "lastname": "Hoang",
        "permission_tier": 1
    }
    token = generate_token(user)
    assert isinstance(token, str)
    assert len(token) > 20

    payload = decode_token(token)
    assert payload["sub"] == "DR_HOANG"
    assert payload["permission_tier"] == 1
    assert payload["firstname"] == "Dr."
