import pytest
import requests
from utils.assertion_manager import assert_error_response


@pytest.mark.negative
def test_remove_track_from_invalid_playlist_should_return_400(user_api_clients, sample_track_uri):
    response = user_api_clients.playlist.remove_tracks_from_playlist(
        "invalid_playlist_123",
        uris=[sample_track_uri]
    )
    assert_error_response(response, expected_status_codes=400, expected_message_substring="Invalid")


@pytest.mark.negative
def test_remove_invalid_track_uri_should_return_400(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.remove_tracks_from_playlist(
        default_playlist_id,
        uris=["spotify:track:INVALID123"]
    )
    assert_error_response(response, expected_status_codes=400, expected_message_substring="invalid")


@pytest.mark.negative
def test_remove_track_without_token_should_return_401(default_playlist_id, sample_track_uri):
    """
    Validate that API returns 401 when authorization is missing.
    """
    payload = {
        "tracks": [{"uri": sample_track_uri}]
    }
    response = requests.delete(
        f"https://api.spotify.com/v1/playlists/{default_playlist_id}/tracks",
        json=payload
    )
    assert_error_response(response, expected_status_codes=401, expected_message_substring="No token")
