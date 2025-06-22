import pytest
from utils.assertion_manager import assert_status_code_ok


@pytest.mark.positive
def test_add_single_track_to_playlist(user_api_clients, valid_track_uri, valid_playlist_id):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=valid_playlist_id,
        uris=[valid_track_uri]
    )
    assert_status_code_ok(response, 201, "Add single track to playlist")


@pytest.mark.positive
def test_add_track_to_playlist_at_position(user_api_clients, valid_track_uri, valid_playlist_id):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=valid_playlist_id,
        uris=[valid_track_uri],
        position=0
    )
    assert_status_code_ok(response, 201, "Add track at position 0")
