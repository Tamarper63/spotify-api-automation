import os
import time
import pytest
from dotenv import load_dotenv

from infra.api_clients.auth_client import AuthClient
from infra.api_clients.playlist_client import PlaylistClient
from infra.api_clients.user_client import UserClient
from infra.auth.token_manager import TokenManager
from infra.http.request_handler import RequestHandler

load_dotenv()

# =======================
# Fixtures
# =======================

@pytest.fixture
def valid_playlist_id() -> str:
    return "7yyTti5oj0AYY68Zlocb1z"


@pytest.fixture
def valid_track_uri() -> str:
    return "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"


@pytest.fixture
def invalid_track_uri() -> str:
    return "spotify:track:invalidtrackuri"


@pytest.fixture(scope="session")
def default_playlist_id() -> str:
    return os.getenv("DEFAULT_PLAYLIST_ID", "7yyTti5oj0AYY68Zlocb1z")


@pytest.fixture(scope="session")
def sample_track_uri() -> str:
    return "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"


@pytest.fixture(scope="session")
def sample_uris() -> list[str]:
    return [
        "spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
        "spotify:track:1301WleyT98MSxVHPZCA6M"
    ]


@pytest.fixture(scope="session")
def token() -> str:
    return TokenManager.get_token()


@pytest.fixture(scope="session")
def user_token() -> str:
    return TokenManager.get_user_token()


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


@pytest.fixture(scope="session")
def user_api_clients(user_request_handler):
    class Clients:
        playlist = PlaylistClient(user_request_handler)
        user = UserClient(user_request_handler)
    return Clients()


# =======================
# HTML Report Hook (pytest-html)
# =======================

def pytest_runtest_logstart(nodeid, location):
    # Initialize a log container per test node
    pytest.current_test_node = {"perf_logs": []}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        perf_logs = getattr(pytest, "current_test_node", {}).get("perf_logs", [])
        if perf_logs:
            # Append all performance logs to HTML report under "API Requests"
            report.sections.append(("API Requests", "\n".join(perf_logs)))


@pytest.fixture
def unauthenticated_playlist_client():
    from infra.http.request_handler import RequestHandler
    from infra.api_clients.playlist_client import PlaylistClient

    return PlaylistClient(RequestHandler(token=""))