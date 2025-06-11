import pytest
from api_clients.auth_client import AuthClient


@pytest.mark.smoke
def test_token_success_with_valid_credentials():
    token = AuthClient().get_access_token()
    assert isinstance(token, str), "Expected access token to be a string"
    assert len(token) > 10, "Access token appears too short"


@pytest.mark.negative
def test_token_fails_with_invalid_credentials(monkeypatch):
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "invalid")
    monkeypatch.setenv("SPOTIFY_CLIENT_SECRET", "invalid")

    with pytest.raises(Exception):
        AuthClient().get_access_token()


