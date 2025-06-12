import pytest


@pytest.mark.smoke
def test_token_success_with_valid_credentials(api_clients):
    token = api_clients.auth.get_access_token()
    assert isinstance(token, str)
    assert len(token) > 10


@pytest.mark.negative
def test_token_fails_with_invalid_credentials(monkeypatch):
    from component.api_clients.auth_client import AuthClient

    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "invalid")
    monkeypatch.setenv("SPOTIFY_CLIENT_SECRET", "invalid")

    client = AuthClient()  # Not from fixture, since we override env vars
    with pytest.raises(Exception):
        client.get_access_token()

