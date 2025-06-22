import pytest
from tests.constants.playlist_constants import DEFAULT_STATUS_OK
from utils.assertion_manager import assert_status_code_ok


@pytest.mark.smoke
@pytest.mark.positive
def test_remove_single_track_should_return_200(user_api_clients, default_playlist_id, sample_track_uri):
    response = user_api_clients.playlist.remove_tracks_from_playlist(
        default_playlist_id,
        uris=[sample_track_uri]
    )
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Remove single track from playlist")


@pytest.mark.positive
def test_remove_multiple_tracks_should_return_200(user_api_clients, default_playlist_id, sample_uris):
    response = user_api_clients.playlist.remove_tracks_from_playlist(
        default_playlist_id,
        uris=sample_uris
    )
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Remove multiple tracks from playlist")
