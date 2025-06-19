import pytest
from infra.auth.token_manager import TokenManager
from infra.api_clients.auth_client import AuthClient
from utils.assertion_manager import (
    assert_token_is_valid,
    assert_error_response,
)

SMOKE_TOKEN_CONTEXT = "Smoke test: Get token with valid credentials"
INVALID_CREDS_CONTEXT = "Invalid credentials"
MISSING_AUTH_HEADER_CONTEXT = "Missing Authorization header"
MISSING_ENV_CONTEXT = "Missing env vars"


# ------------------- POSITIVE TESTS -------------------

@pytest.mark.smoke
@pytest.mark.positive
def test_token_success_with_valid_credentials():
    token = TokenManager.get_token()
    assert_token_is_valid(token)


# ------------------- NEGATIVE TESTS -------------------

@pytest.mark.negative
def test_token_fails_with_invalid_credentials(monkeypatch):
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "invalid_id")
    monkeypatch.setenv("SPOTIFY_CLIENT_SECRET", "invalid_secret")

    client = AuthClient()
    response = client.get_token_response(raw=True)
    assert_error_response(response, expected_status=400, expected_message_substring="invalid client")


@pytest.mark.negative
def test_token_fails_with_missing_env(monkeypatch):
    monkeypatch.delenv("SPOTIFY_CLIENT_ID", raising=False)
    monkeypatch.delenv("SPOTIFY_CLIENT_SECRET", raising=False)

    with pytest.raises(ValueError, match="Missing required credentials"):
        _ = AuthClient()


@pytest.mark.negative
def test_token_fails_with_no_auth_header():
    import requests

    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", data=data)

    assert_error_response(
        response,
        expected_status=400
    )


@pytest.mark.negative
def test_token_fails_with_invalid_url():
    import requests

    headers = {
        "Authorization": "Basic invalid_token",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://accounts.spotify.com/api/invalid_token", headers=headers)

    assert response.status_code in [400, 404, 403]
