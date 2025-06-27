import os
import pytest
from dotenv import load_dotenv
from utils.yaml_loader import load_yaml_data
from infra.api_clients.spotify_client import SpotifyClient
from infra.auth.token_manager import TokenManager
from infra.http.request_handler import RequestHandler

# Load env vars
load_dotenv(override=True)


# === Token & Handlers ===

@pytest.fixture(scope="session")
def token() -> str:
    tok = TokenManager.get_token()
    if not tok:
        pytest.skip("Missing app token")
    return tok


@pytest.fixture(scope="session")
def user_token() -> str:
    utok = TokenManager.get_user_token()
    if not utok:
        pytest.skip("Missing user token")
    return utok


@pytest.fixture(scope="session")
def request_handler(token) -> RequestHandler:
    return RequestHandler(token)


@pytest.fixture(scope="session")
def user_request_handler(user_token) -> RequestHandler:
    return RequestHandler(user_token)


# === Clients ===

@pytest.fixture(scope="session")
def spotify_client(request_handler) -> SpotifyClient:
    return SpotifyClient(request_handler)


@pytest.fixture(scope="session")
def spotify_user_client(user_request_handler) -> SpotifyClient:
    return SpotifyClient(user_request_handler)


# === Track URIs from YAML ===

@pytest.fixture(scope="session")
def sample_uris() -> list[str]:
    data = load_yaml_data("track_uris.yaml")
    return data.get("valid_uris", [])


@pytest.fixture(scope="session")
def invalid_track_uri() -> str:
    data = load_yaml_data("track_uris.yaml")
    return data.get("invalid_uri", "spotify:track:invalid123")


# === Playlist Fixtures ===

@pytest.fixture(scope="session")
def default_playlist_id() -> str:
    return os.getenv("DEFAULT_PLAYLIST_ID", "7yyTti5oj0AYY68Zlocb1z")


@pytest.fixture
def isolated_test_playlist(spotify_user_client, sample_uris):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    playlist_id = spotify_user_client.create_playlist(user_id=user_id, name="Isolated Playlist").json()["id"]
    spotify_user_client.add_tracks_to_playlist(playlist_id, sample_uris)
    yield playlist_id
    spotify_user_client.unfollow_playlist(playlist_id)


@pytest.fixture
def unauthenticated_playlist_client():
    return SpotifyClient(RequestHandler(token=""))


@pytest.fixture
def reorder_ready_playlist(spotify_user_client, sample_uris) -> str:
    """
    Creates a temporary playlist with known tracks to support reorder tests.
    Cleans up by unfollowing the playlist after test.
    """
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    response = spotify_user_client.create_playlist(user_id, name="Reorder Ready Playlist")
    playlist_id = response.json()["id"]
    spotify_user_client.add_tracks_to_playlist(playlist_id, sample_uris)
    yield playlist_id
    spotify_user_client.unfollow_playlist(playlist_id)


def pytest_runtest_logstart(nodeid, location):
    pytest.current_test_node = {"perf_logs": []}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        perf_logs = getattr(pytest, "current_test_node", {}).get("perf_logs", [])
        if perf_logs:
            report.sections.append(("API Requests", "\n".join(perf_logs)))
