import pytest
from dotenv import load_dotenv
from infra.auth.token_manager import TokenManager
from infra.http.request_handler import RequestHandler
from infra.api_clients.spotify_client import SpotifyClient

load_dotenv(override=True)


@pytest.fixture(scope="session")
def token() -> str:
    tok = TokenManager.get_token()
    if not tok:
        pytest.skip("Missing app token")
    return tok


@pytest.fixture(scope="session")
def user_token() -> str:
    try:
        utok = TokenManager.get_user_token()
    except Exception as e:
        print(f"[SKIP] User token error: {e}")
        pytest.skip("Missing or invalid user token")
    if not utok:
        print("[SKIP] No user token provided")
        pytest.skip("Missing user token")
    return utok


@pytest.fixture(scope="function")
def request_handler(token) -> RequestHandler:
    return RequestHandler(token)


@pytest.fixture(scope="function")
def user_request_handler(user_token) -> RequestHandler:
    return RequestHandler(user_token)


@pytest.fixture(scope="function")
def spotify_client(request_handler) -> SpotifyClient:
    return SpotifyClient(request_handler)


@pytest.fixture(scope="function")
def spotify_user_client(user_request_handler) -> SpotifyClient:
    return SpotifyClient(user_request_handler)
