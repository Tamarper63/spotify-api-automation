import pytest
from infra.auth.token_manager import TokenManager
from infra.api_clients.auth_client import AuthClient
from utils.assertion_manager import assert_token_is_valid


@pytest.mark.smoke
def test_token_success_with_valid_credentials():
    token = TokenManager.get_token()
    assert_token_is_valid(token)


@pytest.mark.negative
def test_token_fails_with_invalid_credentials(monkeypatch):
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "invalid")
    monkeypatch.setenv("SPOTIFY_CLIENT_SECRET", "invalid")

    client = AuthClient()
    with pytest.raises(Exception):
        client.get_token_response()

