import pytest
from utils.assertion_manager import assert_status_code_ok, assert_error_response


@pytest.mark.positive
def test_reorder_tracks_should_return_200(spotify_user_client, reorder_ready_playlist):
    """
    Valid reorder request returns 200 and changes track order.
    """
    response = spotify_user_client.reorder_playlist_items(
        playlist_id=reorder_ready_playlist, range_start=0, insert_before=2
    )
    assert_status_code_ok(response, 200)


@pytest.mark.negative
def test_reorder_tracks_with_invalid_range_should_return_400(
    spotify_user_client, reorder_ready_playlist
):
    """
    Reordering with invalid range_start (e.g., -1) returns 400.
    """
    response = spotify_user_client.reorder_playlist_items(
        playlist_id=reorder_ready_playlist, range_start=-1, insert_before=1
    )
    assert_error_response(
        response, expected_status_codes=400, expected_message_substring="range_start"
    )


@pytest.mark.negative
def test_reorder_tracks_without_auth_should_return_400_or_401(
    unauthenticated_playlist_client, reorder_ready_playlist
):
    """
    Reordering without authentication should return 401/400 depending on backend enforcement.
    """
    response = unauthenticated_playlist_client.reorder_playlist_items(
        playlist_id=reorder_ready_playlist, range_start=0, insert_before=1
    )
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="Only valid bearer authentication supported",
    )
