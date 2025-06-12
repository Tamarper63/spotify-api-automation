
import pytest
from component.api_clients.auth_client import AuthClient
from component.api_clients.playlist_client import PlaylistClient
from infra.request_handler import RequestHandler


@pytest.fixture(scope="session")
def token() -> str:
    return AuthClient().get_access_token()


@pytest.fixture(scope="session")
def request_handler(token) -> RequestHandler:
    return RequestHandler(token)


@pytest.fixture(scope="session")
def api_clients(request_handler):
    class Clients:
        auth = AuthClient()
        playlist = PlaylistClient(request_handler)
        # Add more clients here in the future

    return Clients()
