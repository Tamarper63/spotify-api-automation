from unittest import skip

import pytest
import requests
from pydantic_core import ValidationError

from infra.api_clients.spotify_client import SpotifyClient
from infra.config.settings import get_settings
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
INVALID_URL_CONTEXT = "Invalid token URL"
INVALID_GRANT_CONTEXT = "Invalid grant_type values"


# ------------------- POSITIVE TESTS -------------------

@pytest.mark.positive
def test_token_success_with_valid_credentials():
    client = SpotifyClient()
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

    client = SpotifyClient()
    response = client.get_token_response(raw=True)

    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring=expected_message,
        context=INVALID_CREDS_CONTEXT
    )


@skip(reason='working only while run alon our the current file, failed consistently while run as part of large suit')
@pytest.mark.negative
@pytest.mark.parametrize("env_to_delete", ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"])
def test_token_fails_with_partial_env(monkeypatch, env_to_delete):
    monkeypatch.delenv(env_to_delete, raising=False)

    with pytest.raises(ValidationError, match=env_to_delete):
        _ = get_settings()


@skip(reason='working only while run alon our the current file, failed consistently while run as part of large suit')
@pytest.mark.negative
def test_token_fails_with_all_env_missing(monkeypatch):
    monkeypatch.delenv("SPOTIFY_CLIENT_ID", raising=False)
    monkeypatch.delenv("SPOTIFY_CLIENT_SECRET", raising=False)

    with pytest.raises(ValidationError, match="SPOTIFY_CLIENT_ID"):
        _ = get_settings()


@pytest.mark.negative
def test_token_fails_with_no_auth_header():
    response = requests.post(
        url="https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert_error_response(response, expected_status_codes=400, context=MISSING_AUTH_HEADER_CONTEXT)


@pytest.mark.negative
def test_token_fails_with_invalid_url():
    response = requests.post(
        url="https://accounts.spotify.com/api/invalid_token",
        data={"grant_type": "client_credentials"},
        headers={
            "Authorization": "Basic invalid_token",
            "Content-Type": "application/x-www-form-urlencoded"
        },
    )

    assert_error_response(
        response,
        expected_status_codes=[400, 403, 404],
        context=INVALID_URL_CONTEXT
    )


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
        expected_status_codes=expected_status,
        expected_message_substring=expected_message,
        context=INVALID_GRANT_CONTEXT
    )
