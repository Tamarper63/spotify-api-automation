import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response,
    assert_keys_exist,
)


# ===========================
# Positive Tests
# ===========================


@pytest.mark.positive
@pytest.mark.parametrize("limit", [1, 5, 10])
def test_get_playlist_items_with_limit_should_match_response(
    spotify_user_client, default_playlist_id, limit
):
    response = spotify_user_client.get_playlist_items(
        playlist_id=default_playlist_id, limit=limit
    )
    assert_status_code_ok(response, 200, "Get playlist items with limit")
    json = response.json()
    assert_keys_exist(json, ["items", "limit", "href"])
    assert json["limit"] == limit


@pytest.mark.positive
@pytest.mark.parametrize("offset", [0, 1, 2])
def test_get_playlist_items_with_offset_should_return_items(
    spotify_user_client, default_playlist_id, offset
):
    response = spotify_user_client.get_playlist_items(
        playlist_id=default_playlist_id, limit=1, offset=offset
    )
    assert_status_code_ok(response, 200, "Get playlist items with offset")
    json = response.json()
    assert_keys_exist(json, ["items"])


@pytest.mark.positive
def test_get_playlist_items_with_all_params_should_succeed(
    spotify_user_client, default_playlist_id
):
    response = spotify_user_client.get_playlist_items(
        playlist_id=default_playlist_id,
        market="US",
        fields="items.track.name,total",
        limit=3,
        offset=1,
    )
    assert_status_code_ok(response, 200, "Get playlist items with full param set")
    json = response.json()
    assert_keys_exist(json, ["items", "total"])


# ===========================
# Negative Tests
# ===========================


@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", ["invalid_id", "123", "!!!"])
def test_get_playlist_items_with_invalid_id_should_return_400(
    spotify_user_client, invalid_id
):
    response = spotify_user_client.get_playlist_items(playlist_id=invalid_id)
    assert_error_response(
        response, expected_status_codes=400, expected_message_substring="invalid"
    )


@pytest.mark.negative
@pytest.mark.parametrize("bad_limit", [-10, 0, 1001])
def test_get_playlist_items_with_invalid_limit_should_return_400(
    spotify_user_client, default_playlist_id, bad_limit
):
    response = spotify_user_client.get_playlist_items(
        playlist_id=default_playlist_id, limit=bad_limit
    )
    assert_error_response(
        response, expected_status_codes=400, expected_message_substring="limit"
    )


@pytest.mark.negative
def test_get_playlist_items_without_auth_should_return_400(
    unauthenticated_playlist_client, default_playlist_id
):
    response = unauthenticated_playlist_client.get_playlist_items(default_playlist_id)
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="Only valid bearer",
    )
