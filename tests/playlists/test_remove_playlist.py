import pytest
import requests

from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response
)


@pytest.mark.smoke
@pytest.mark.positive
def test_remove_single_track_should_return_200(user_api_clients, default_playlist_id, sample_track_uri):
    response = user_api_clients.playlist.remove_tracks_from_playlist(
        default_playlist_id,
        uris=[sample_track_uri]
    )
    assert_status_code_ok(response, 200, "Remove single track")


@pytest.mark.positive
def test_remove_multiple_tracks_should_return_200(user_api_clients, default_playlist_id, sample_uris):
    response = user_api_clients.playlist.remove_tracks_from_playlist(
        default_playlist_id,
        uris=sample_uris
    )
    assert_status_code_ok(response, 200, "Remove multiple tracks")


@pytest.mark.negative
def test_remove_track_from_invalid_playlist_should_return_404(user_api_clients, sample_track_uri):
    response = user_api_clients.playlist.remove_tracks_from_playlist(
        "invalid_playlist_123",
        uris=[sample_track_uri]
    )
    assert_error_response(response, 400)


@pytest.mark.negative
def test_remove_invalid_track_uri_should_return_400(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.remove_tracks_from_playlist(
        default_playlist_id,
        uris=["spotify:track:INVALID123"]
    )
    assert_error_response(response, 400)


@pytest.mark.negative
def test_remove_track_without_token_should_return_401(default_playlist_id, sample_track_uri):
    payload = {
        "tracks": [{"uri": sample_track_uri}]
    }
    response = requests.delete(
        f"https://api.spotify.com/v1/playlists/{default_playlist_id}/tracks",
        json=payload  # No auth header
    )
    assert_error_response(response, 401)
