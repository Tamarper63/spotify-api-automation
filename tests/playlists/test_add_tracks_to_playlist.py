import pytest
from utils.assertion_manager import assert_status_code_ok, assert_error_response

VALID_PLAYLIST_ID = "7yyTti5oj0AYY68Zlocb1z"
VALID_TRACK_URI = "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
INVALID_TRACK_URI = "spotify:track:invalidtrackuri"


@pytest.mark.positive
def test_add_single_track_to_playlist(user_api_clients):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=VALID_PLAYLIST_ID,
        uris=[VALID_TRACK_URI]
    )
    assert_status_code_ok(response, 201)


@pytest.mark.positive
def test_add_track_to_playlist_at_position(user_api_clients):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=VALID_PLAYLIST_ID,
        uris=[VALID_TRACK_URI],
        position=0
    )
    assert_status_code_ok(response, 201)


@pytest.mark.negative
def test_add_invalid_track_to_playlist(user_api_clients):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=VALID_PLAYLIST_ID,
        uris=[INVALID_TRACK_URI]
    )
    assert response.status_code in [400, 403, 404]


@pytest.mark.negative
def test_add_tracks_with_empty_uri_list(user_api_clients):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=VALID_PLAYLIST_ID,
        uris=[]
    )
    assert response.status_code in [400, 422]


@pytest.mark.negative
def test_add_tracks_without_auth():
    from infra.http.request_handler import RequestHandler
    from infra.api_clients.playlist_client import PlaylistClient

    handler = RequestHandler(token="")
    client = PlaylistClient(handler)
    response = client.add_tracks_to_playlist(
        playlist_id=VALID_PLAYLIST_ID,
        uris=[VALID_TRACK_URI]
    )
    assert_error_response(response, 400)
