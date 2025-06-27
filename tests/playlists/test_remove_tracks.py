import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response, ensure_tracks_exist_in_playlist,
)


@pytest.mark.positive
def test_remove_existing_tracks_should_return_200(user_api_clients, default_playlist_id, sample_uris):
    """
    Preconditions: Ensure tracks exist in the playlist.
    Then: Remove the tracks and assert success.
    """
    ensure_tracks_exist_in_playlist(user_api_clients, default_playlist_id, sample_uris)

    response = user_api_clients.playlist.remove_tracks_from_playlist(
        playlist_id=default_playlist_id,
        uris=sample_uris
    )
    assert_status_code_ok(response, 200, "Remove existing tracks")


@pytest.mark.negative
def test_remove_tracks_without_auth_should_return_400(unauthenticated_playlist_client, default_playlist_id, sample_uris):
    """
    Attempt to remove tracks using an empty/invalid token.
    """
    response = unauthenticated_playlist_client.remove_tracks_from_playlist(
        playlist_id=default_playlist_id,
        uris=sample_uris
    )
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="Only valid bearer authentication supported"
    )


@pytest.mark.negative
def test_remove_tracks_with_invalid_uri_should_return_400(user_api_clients, default_playlist_id, invalid_track_uri):
    """
    Attempt to remove a track using an invalid URI format.
    """
    response = user_api_clients.playlist.remove_tracks_from_playlist(
        playlist_id=default_playlist_id,
        uris=[invalid_track_uri]
    )
    assert_error_response(response, expected_status_codes=400, expected_message_substring="invalid")
