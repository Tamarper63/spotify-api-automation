import pytest

from infra.auth.token_manager import TokenManager
from infra.api_clients.auth_client import AuthClient
from utils.assertion_manager import assert_token_is_valid


INVALID_CLIENT_ID = "invalid"
INVALID_CLIENT_SECRET = "invalid"
MISSING_ENV_VARS = ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"]


@pytest.mark.smoke
@pytest.mark.positive
def test_get_token_success_with_valid_credentials():
    """
    Ensure token is retrieved successfully using valid credentials.
    """
    token = TokenManager.get_token()
    assert_token_is_valid(token)


@pytest.mark.negative
def test_get_token_with_invalid_credentials_should_raise(monkeypatch):
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", INVALID_CLIENT_ID)
    monkeypatch.setenv("SPOTIFY_CLIENT_SECRET", INVALID_CLIENT_SECRET)

    client = AuthClient()
    with pytest.raises(Exception, match="(invalid|unauthorized|400)"):
        client.get_token_response()


@pytest.mark.negative
def test_get_token_with_missing_credentials_should_raise(monkeypatch):
    for var in MISSING_ENV_VARS:
        monkeypatch.delenv(var, raising=False)

    client = AuthClient()
    with pytest.raises(Exception, match="(missing|credentials|400)"):
        client.get_token_response()
