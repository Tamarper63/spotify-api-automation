import pytest
from dotenv import load_dotenv

from infra.auth.token_manager import TokenManager
from infra.http.request_handler import RequestHandler
from infra.api_clients.spotify_client import SpotifyClient
from infra.config.loader import load_config
from utils.log_utils import log_warning

load_dotenv(override=True)


@pytest.fixture(scope="session")
def config():
    try:
        return load_config()
    except Exception as e:
        log_warning(f"[CONFIG ERROR] Failed to load config: {e}")
        pytest.skip("❌ Failed to load configuration")


@pytest.fixture(scope="session")
def token(config) -> str:
    try:
        tok = TokenManager.get_token(config)
    except Exception as e:
        log_warning(f"[SKIP] App token error: {e}")
        pytest.skip("❌ Failed to obtain app token")
    if not tok:
        log_warning("[SKIP] App token returned empty string")
        pytest.skip("❌ App token is empty")
    return tok


@pytest.fixture(scope="session")
def user_token(config) -> str:
    try:
        utok = TokenManager.get_user_token(config)
    except Exception as e:
        log_warning(f"[SKIP] User token error: {e}")
        pytest.skip("❌ Invalid or missing user token")
    if not utok:
        log_warning("[SKIP] No user token provided (empty string)")
        pytest.skip("❌ User token not provided")
    return utok


@pytest.fixture(scope="function")
def request_handler(token) -> RequestHandler:
    return RequestHandler(token=token)


@pytest.fixture(scope="function")
def user_request_handler(user_token) -> RequestHandler:
    return RequestHandler(token=user_token)


@pytest.fixture(scope="function")
def spotify_client(request_handler) -> SpotifyClient:
    return SpotifyClient(request_handler)


@pytest.fixture(scope="function")
def spotify_user_client(user_request_handler) -> SpotifyClient:
    return SpotifyClient(user_request_handler)
