import pytest
import requests
from utils.assertion_manager import assert_status_code_ok, assert_error_response


@pytest.mark.positive
def test_add_tracks_should_return_201(
    spotify_user_client, default_playlist_id, sample_uris
):
    response = spotify_user_client.add_tracks_to_playlist(
        playlist_id=default_playlist_id, uris=sample_uris
    )
    assert_status_code_ok(response, 201, "Add tracks to playlist")


@pytest.mark.positive
def test_add_tracks_with_position_should_return_201(
    spotify_user_client, default_playlist_id, sample_uris
):
    response = spotify_user_client.add_tracks_to_playlist(
        playlist_id=default_playlist_id, uris=sample_uris, position=0
    )
    assert_status_code_ok(response, 201, "Add tracks with position")


@pytest.mark.negative
def test_add_tracks_without_auth(
    unauthenticated_playlist_client, default_playlist_id, sample_uris
):
    response = unauthenticated_playlist_client.add_tracks_to_playlist(
        playlist_id=default_playlist_id, uris=sample_uris
    )
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="Only valid bearer",
    )


@pytest.mark.negative
def test_add_tracks_with_no_authorization_header(default_playlist_id, sample_uris):
    response = requests.post(
        url=f"https://api.spotify.com/v1/playlists/{default_playlist_id}/tracks",
        json={"uris": sample_uris},
        headers={"Content-Type": "application/json"},
    )
    assert_error_response(response, expected_status_codes=401)


@pytest.mark.negative
def test_add_tracks_with_invalid_uri(
    spotify_user_client, default_playlist_id, invalid_track_uri
):
    response = spotify_user_client.add_tracks_to_playlist(
        playlist_id=default_playlist_id, uris=[invalid_track_uri]
    )
    assert_error_response(response, expected_status_codes=400)
