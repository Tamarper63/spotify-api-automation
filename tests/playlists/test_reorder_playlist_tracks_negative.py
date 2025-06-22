import pytest
from utils.assertion_manager import assert_error_response



@pytest.mark.negative
def test_reorder_tracks_with_invalid_range_start_should_return_400(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_playlist_items(
        playlist_id=default_playlist_id,
        range_start=999,  # Invalid
        insert_before=0
    )
    assert_error_response(response, expected_status_codes=400, expected_message_substring="out of bounds")


@pytest.mark.negative
def test_reorder_tracks_with_invalid_insert_before_should_return_400(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_playlist_items(
        playlist_id=default_playlist_id,
        range_start=0,
        insert_before=999  # Invalid
    )
    assert_error_response(response, expected_status_codes=400, expected_message_substring="out of bounds")


@pytest.mark.negative
def test_reorder_tracks_missing_token_should_return_401(default_playlist_id):
    from requests import put

    payload = {
        "range_start": 0,
        "insert_before": 1
    }
    response = put(
        f"https://api.spotify.com/v1/playlists/{default_playlist_id}/tracks",
        json=payload
    )
    assert_error_response(response, expected_status_codes=401, expected_message_substring="No token")
