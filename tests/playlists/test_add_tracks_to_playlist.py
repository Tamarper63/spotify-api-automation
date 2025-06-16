import pytest
from utils.assertion_manager import assert_status_code_ok, assert_error_response


@pytest.mark.positive
def test_add_single_track_to_playlist(user_api_clients, valid_track_uri, valid_playlist_id):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=valid_playlist_id,
        uris=[valid_track_uri]
    )
    assert_status_code_ok(response, 201)


@pytest.mark.positive
def test_add_track_to_playlist_at_position(user_api_clients, valid_track_uri, valid_playlist_id):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=valid_playlist_id,
        uris=[valid_track_uri],
        position=0
    )
    assert_status_code_ok(response, 201)


@pytest.mark.negative
def test_add_invalid_track_to_playlist(user_api_clients, invalid_track_uri, valid_playlist_id):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=valid_playlist_id,
        uris=[invalid_track_uri]
    )
    assert response.status_code in [400, 403, 404]


@pytest.mark.negative
def test_add_tracks_with_empty_uri_list(user_api_clients, valid_playlist_id):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=valid_playlist_id,
        uris=[]
    )
    assert response.status_code in [400, 422]


@pytest.mark.negative
def test_add_tracks_without_auth(valid_track_uri, valid_playlist_id):
    from infra.http.request_handler import RequestHandler
    from infra.api_clients.playlist_client import PlaylistClient

    handler = RequestHandler(token="")
    client = PlaylistClient(handler)
    response = client.add_tracks_to_playlist(
        playlist_id=valid_playlist_id,
        uris=[valid_track_uri]
    )
    assert_error_response(response, 400)
