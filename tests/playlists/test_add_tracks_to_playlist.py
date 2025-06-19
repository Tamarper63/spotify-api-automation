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
    assert_error_response(response, expected_status_codes=[400, 403, 404])


@pytest.mark.negative
def test_add_tracks_with_empty_uri_list(user_api_clients, valid_playlist_id):
    response = user_api_clients.playlist.add_tracks_to_playlist(
        playlist_id=valid_playlist_id,
        uris=[]
    )
    assert_error_response(response, expected_status_codes=[400, 422])


@pytest.mark.negative
def test_add_tracks_without_auth(unauthenticated_playlist_client, valid_track_uri, valid_playlist_id):
    response = unauthenticated_playlist_client.add_tracks_to_playlist(
        playlist_id=valid_playlist_id,
        uris=[valid_track_uri]
    )
    assert_error_response(response, expected_status=400)
