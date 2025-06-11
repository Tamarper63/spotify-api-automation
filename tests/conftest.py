# tests/conftest.py
import pytest
from infra.request_handler import RequestHandler
from api_clients.playlist_client import PlaylistClient
from api_clients.auth_client import AuthClient


@pytest.fixture(scope="session")
def token():
    return AuthClient().get_access_token()


@pytest.fixture(scope="session")
def request_handler(token):
    return RequestHandler(token)


@pytest.fixture(scope="session")
def api_clients(request_handler):
    class Clients:
        playlist = PlaylistClient(request_handler)
        # Add more as needed

    return Clients()
