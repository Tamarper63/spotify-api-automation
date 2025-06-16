import pytest
from utils.assertion_manager import assert_status_code_ok, assert_error_response


@pytest.mark.positive
def test_replace_tracks_success(user_api_clients, default_playlist_id, sample_uris):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        uris=sample_uris
    )
    assert_status_code_ok(response, 200, "Replace all tracks")


@pytest.mark.positive
def test_reorder_tracks_with_minimal_params(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        range_start=0,
        insert_before=1
    )
    assert_status_code_ok(response, 200, "Reorder tracks minimal params")


@pytest.mark.positive
def test_reorder_tracks_with_range_length(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        range_start=0,
        insert_before=2,
        range_length=1
    )
    assert_status_code_ok(response, 200, "Reorder with range_length")


@pytest.mark.negative
def test_replace_tracks_with_invalid_uri(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        uris=["spotify:track:INVALID"]
    )
    assert_error_response(response, 400)


@pytest.mark.negative
def test_reorder_with_missing_insert_before(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        range_start=1
        # Missing insert_before
    )
    assert_error_response(response, 400)


@pytest.mark.negative
def test_reorder_with_invalid_range(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        range_start=100,  # Likely out of bounds
        insert_before=1
    )
    assert response.status_code in [400, 403]


@pytest.mark.negative
def test_reorder_without_auth(default_playlist_id, sample_uris):
    from infra.http.request_handler import RequestHandler
    from infra.api_clients.playlist_client import PlaylistClient

    unauth = PlaylistClient(RequestHandler(token=""))
    response = unauth.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        uris=sample_uris
    )
    assert response.status_code == 400
