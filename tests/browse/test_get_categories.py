import pytest
from utils.assertion_manager import assert_status_code_ok, assert_keys_exist
import requests


@pytest.mark.contract
@pytest.mark.integration
@pytest.mark.parametrize("locale, limit, offset", [
    ("en_US", 5, 0),
    ("es_MX", 10, 5),
])
def test_get_categories_ok(user_api_clients, locale, limit, offset):
    response = user_api_clients.browse.get_categories(locale=locale, limit=limit, offset=offset)
    assert_status_code_ok(response, 200)
    payload = response.json()
    assert "categories" in payload
    assert_keys_exist(payload["categories"], ["items", "limit", "offset", "total"])


@pytest.mark.negative
def test_get_categories_unauthorized():
    response = requests.get("https://api.spotify.com/v1/browse/categories")
    assert response.status_code in (401, 403)
