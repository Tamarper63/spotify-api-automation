import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_keys_exist,
    assert_json_field_equals
)


@pytest.mark.contract
def test_get_playlist_items_contract(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.get_playlist_items(default_playlist_id)
    assert_status_code_ok(response, 200, "Get playlist items contract")

    response_json = response.json()
    assert_keys_exist(response_json, ["items", "href", "limit", "total"])
    assert isinstance(response_json["items"], list)


@pytest.mark.positive
@pytest.mark.parametrize("market, limit, offset", [
    ("US", 5, 0),
    ("IL", 10, 5),
])
def test_get_playlist_items_with_optional_params(user_api_clients, default_playlist_id, market, limit, offset):
    response = user_api_clients.playlist.get_playlist_items(
        playlist_id=default_playlist_id,
        market=market,
        limit=limit,
        offset=offset
    )
    assert_status_code_ok(response, 200, "Get playlist items with optional params")
    assert_keys_exist(response.json(), ["items", "href", "limit", "total"])
