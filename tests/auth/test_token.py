import pytest
import requests
from unittest import skip
from pydantic_core import ValidationError

from infra.api_clients.spotify_client import SpotifyClient
from infra.config.loader import load_config
from infra.models.token_response import TokenResponse
from utils.assertion_manager import (
    assert_token_is_valid,
    assert_error_response,
    assert_response_schema,
)

# --- Context Constants ---

SMOKE_TOKEN_CONTEXT = "Smoke test: Get token with valid credentials"
INVALID_CREDS_CONTEXT = "Invalid credentials"
MISSING_AUTH_HEADER_CONTEXT = "Missing Authorization header"
MISSING_ENV_CONTEXT = "Missing environment variables"
INVALID_URL_CONTEXT = "Invalid token URL"
INVALID_GRANT_CONTEXT = "Invalid grant_type values"

# --- Positive Tests ---


@pytest.mark.positive
def test_token_success_with_valid_credentials():
    """
    Test successful token retrieval with valid client credentials.
    Validates schema and token format.
    """
    client = SpotifyClient()
    full_response = client.get_token_response()

    assert_response_schema(full_response, TokenResponse, context=SMOKE_TOKEN_CONTEXT)
    assert_token_is_valid(full_response["access_token"])


# --- Negative Tests ---


@pytest.mark.negative
@pytest.mark.parametrize(
    "client_id, client_secret, expected_message",
    [
        ("invalid_id", "invalid_secret", "invalid client"),
    ],
)
def test_token_invalid_credentials(client_id, client_secret, expected_message):
    """
    Test token request failure with invalid client_id and client_secret.
    Verifies error message content and HTTP status 400.
    """
    client = SpotifyClient(client_id=client_id, client_secret=client_secret)
    response = client.get_token_response(raw=True)

    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring=expected_message,
        context=INVALID_CREDS_CONTEXT,
    )


@skip(reason="working only when run alone; fails in full suite due to .env caching")
@pytest.mark.negative
@pytest.mark.parametrize(
    "env_to_delete", ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"]
)
def test_token_fails_with_partial_env(monkeypatch, env_to_delete):
    """
    Test validation failure if partial environment variables are missing.
    Expects Pydantic ValidationError mentioning the missing env var.
    """
    monkeypatch.delenv(env_to_delete, raising=False)

    with pytest.raises(ValidationError, match=env_to_delete):
        _ = load_config()


@skip(reason="working only when run alone; fails in full suite due to .env caching")
@pytest.mark.negative
def test_token_fails_with_all_env_missing(monkeypatch):
    """
    Test validation failure if all required environment variables are missing.
    Expects Pydantic ValidationError mentioning SPOTIFY_CLIENT_ID.
    """
    monkeypatch.delenv("SPOTIFY_CLIENT_ID", raising=False)
    monkeypatch.delenv("SPOTIFY_CLIENT_SECRET", raising=False)

    with pytest.raises(ValidationError, match="SPOTIFY_CLIENT_ID"):
        _ = load_config()


@pytest.mark.negative
def test_token_fails_with_no_auth_header():
    """
    Test token request failure due to missing Authorization header.
    Expects HTTP 400 and relevant error context.
    """
    response = requests.post(
        url="https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert_error_response(
        response, expected_status_codes=400, context=MISSING_AUTH_HEADER_CONTEXT
    )


@pytest.mark.negative
def test_token_fails_with_invalid_url():
    """
    Test token request failure on invalid endpoint URL.
    Verifies response is in HTTP 400, 403, or 404 range.
    """
    response = requests.post(
        url="https://accounts.spotify.com/api/invalid_token",
        data={"grant_type": "client_credentials"},
        headers={
            "Authorization": "Basic invalid_token",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert_error_response(
        response, expected_status_codes=[400, 403, 404], context=INVALID_URL_CONTEXT
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "grant_type, expected_status, expected_message",
    [
        (None, 400, "grant_type parameter is missing"),
        ("", 400, "grant_type parameter is missing"),
        ("invalid_grant", 400, "grant_type invalid_grant is not supported"),
    ],
)
def test_token_fails_with_invalid_grant_type(
    grant_type, expected_status, expected_message
):
    """
    Test token request failure for invalid or missing grant_type values.
    Validates error message substring and status code.
    """
    headers = {
        "Authorization": "Basic invalid_token",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": grant_type} if grant_type is not None else {}

    response = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data
    )

    assert_error_response(
        response,
        expected_status_codes=expected_status,
        expected_message_substring=expected_message,
        context=INVALID_GRANT_CONTEXT,
    )
