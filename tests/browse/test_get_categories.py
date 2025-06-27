# tests/browse/test_get_categories.py

import pytest
from utils.assertion_manager import assert_status_code_ok, assert_keys_exist
from infra.http.request_handler import RequestHandler
from infra.api_clients.spotify_client import SpotifyClient


@pytest.mark.contract
@pytest.mark.integration
@pytest.mark.parametrize("locale, limit, offset", [
    ("en_US", 5, 0),
    ("es_MX", 10, 5),
])
def test_get_categories_ok(user_api_clients, locale, limit, offset):
    response = user_api_clients.spotify.get_categories(locale=locale, limit=limit, offset=offset)
    assert_status_code_ok(response, 200)
    payload = response.json()
    assert "categories" in payload
    assert_keys_exist(payload["categories"], ["items", "limit", "offset", "total"])


@pytest.mark.negative
def test_get_categories_unauthorized():
    """
    Verify that omitting the Authorization header results in unauthorized access.
    """
    client = SpotifyClient(request_handler=RequestHandler(token=""))  # empty token
    response = client.get_categories()
    assert response.status_code in (400, 401, 403)
