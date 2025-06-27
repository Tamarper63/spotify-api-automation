import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response,
    assert_keys_exist,
)


@pytest.mark.positive
@pytest.mark.parametrize("limit", [5, 10])
def test_get_playlist_items_limit_match_response(user_api_clients, default_playlist_id, limit):
    response = user_api_clients.playlist.get_playlist_items(
        playlist_id=default_playlist_id,
        limit=limit
    )
    assert_status_code_ok(response, 200, "Get playlist items with limit")
    json = response.json()
    assert_keys_exist(json, ["items", "limit", "href"])
    assert json["limit"] == limit, f"❌ Limit mismatch: expected {limit}, got {json['limit']}"


@pytest.mark.positive
def test_get_playlist_items_with_offset(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.get_playlist_items(
        playlist_id=default_playlist_id,
        limit=1,
        offset=1
    )
    assert_status_code_ok(response, 200, "Get playlist items with offset")
    assert "items" in response.json()


@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", ["invalid_id", "123", "!!!"])
def test_get_playlist_items_with_invalid_id_should_return_400(user_api_clients, invalid_id):
    response = user_api_clients.playlist.get_playlist_items(playlist_id=invalid_id)
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="invalid"
    )


@pytest.mark.negative
def test_get_playlist_items_with_invalid_limit_should_return_400(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.get_playlist_items(
        playlist_id=default_playlist_id,
        limit=-5
    )
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="limit"
    )
