import os
import pytest

from infra.api_clients.auth_client import AuthClient
from infra.api_clients.playlist_client import PlaylistClient
from infra.api_clients.user_client import UserClient
from infra.auth.token_manager import TokenManager
from infra.http.request_handler import RequestHandler
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def valid_playlist_id() -> str:
    return "7yyTti5oj0AYY68Zlocb1z"


@pytest.fixture
def valid_track_uri() -> str:
    return "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"


@pytest.fixture
def invalid_track_uri() -> str:
    return "spotify:track:invalidtrackuri"


# Use a real playlist ID you control or create one dynamically in a setup
@pytest.fixture(scope="session")
def default_playlist_id() -> str:
    return "7yyTti5oj0AYY68Zlocb1z"  # replace with your test playlist ID


@pytest.fixture(scope="session")
def sample_track_uri() -> str:
    return "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"  # valid public track


@pytest.fixture(scope="session")
def sample_uris() -> list[str]:
    return [
        "spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
        "spotify:track:1301WleyT98MSxVHPZCA6M"
    ]


# Default client credentials token (for read-only endpoints)
@pytest.fixture(scope="session")
def token() -> str:
    return TokenManager.get_token()


@pytest.fixture(scope="session")
def user_token() -> str:
    return TokenManager.get_user_token()


@pytest.fixture(scope="session")
def default_playlist_id():
    return os.getenv("DEFAULT_PLAYLIST_ID")


@pytest.fixture(scope="session")
def request_handler(token) -> RequestHandler:
    return RequestHandler(token)


@pytest.fixture(scope="session")
def user_request_handler(user_token) -> RequestHandler:
    return RequestHandler(user_token)


@pytest.fixture(scope="session")
def api_clients(request_handler):
    class Clients:
        auth = AuthClient()
        playlist = PlaylistClient(request_handler)
        user = UserClient(request_handler)

    return Clients()


# 🔐 Use this in tests that require user-scoped endpoints
@pytest.fixture(scope="session")
def user_api_clients(user_request_handler):
    class Clients:
        playlist = PlaylistClient(user_request_handler)
        user = UserClient(user_request_handler)

    return Clients()
