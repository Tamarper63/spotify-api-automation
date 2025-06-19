import pytest
import requests

from infra.api_clients.auth_client import AuthClient
from infra.models.token_response import TokenResponse
from utils.assertion_manager import (
    assert_token_is_valid,
    assert_error_response,
    assert_response_schema,
)

# ------------------- Context Constants -------------------

SMOKE_TOKEN_CONTEXT = "Smoke test: Get token with valid credentials"
INVALID_CREDS_CONTEXT = "Invalid credentials"
MISSING_AUTH_HEADER_CONTEXT = "Missing Authorization header"
MISSING_ENV_CONTEXT = "Missing environment variables"


# ------------------- POSITIVE TESTS -------------------

@pytest.mark.positive
def test_token_success_with_valid_credentials():
    client = AuthClient()
    full_response = client.get_token_response()

    assert_response_schema(full_response, TokenResponse, context=SMOKE_TOKEN_CONTEXT)
    assert_token_is_valid(full_response["access_token"])


# ------------------- NEGATIVE TESTS -------------------

@pytest.mark.negative
@pytest.mark.parametrize("client_id, client_secret, expected_message", [
    ("invalid_id", "invalid_secret", "invalid client"),
])
def test_token_invalid_credentials(monkeypatch, client_id, client_secret, expected_message):
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", client_id)
    monkeypatch.setenv("SPOTIFY_CLIENT_SECRET", client_secret)

    client = AuthClient()
    response = client.get_token_response(raw=True)

    assert_error_response(response, expected_status=400, expected_message_substring=expected_message)


@pytest.mark.negative
@pytest.mark.parametrize("env_to_delete", ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"])
def test_token_fails_with_partial_env(monkeypatch, env_to_delete):
    monkeypatch.delenv(env_to_delete, raising=False)
    with pytest.raises(ValueError, match="Missing required credentials"):
        _ = AuthClient()


@pytest.mark.negative
def test_token_fails_with_all_env_missing(monkeypatch):
    monkeypatch.delenv("SPOTIFY_CLIENT_ID", raising=False)
    monkeypatch.delenv("SPOTIFY_CLIENT_SECRET", raising=False)
    with pytest.raises(ValueError, match="Missing required credentials"):
        _ = AuthClient()


@pytest.mark.negative
def test_token_fails_with_no_auth_header():
    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", data=data)

    assert_error_response(response, expected_status=400)


@pytest.mark.negative
def test_token_fails_with_invalid_url():
    headers = {
        "Authorization": "Basic invalid_token",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://accounts.spotify.com/api/invalid_token", headers=headers)
    assert response.status_code in [400, 403, 404]


@pytest.mark.negative
@pytest.mark.parametrize("grant_type, expected_status, expected_message", [
    (None, 400, "grant_type parameter is missing"),
    ("", 400, "grant_type parameter is missing"),
    ("invalid_grant", 400, "grant_type invalid_grant is not supported"),
])
def test_token_fails_with_invalid_grant_type(grant_type, expected_status, expected_message):
    headers = {
        "Authorization": "Basic invalid_token",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": grant_type} if grant_type is not None else {}

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    assert_error_response(
        response,
        expected_status=expected_status,
        expected_message_substring=expected_message
    )
