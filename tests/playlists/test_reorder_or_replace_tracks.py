import pytest

from tests.constants.playlist_constants import DEFAULT_STATUS_OK
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response,
)
from infra.http.request_handler import RequestHandler
from infra.api_clients.playlist_client import PlaylistClient


@pytest.mark.positive
def test_replace_tracks_should_return_200(user_api_clients, default_playlist_id, sample_uris):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        uris=sample_uris
    )
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Replace all tracks in playlist")


@pytest.mark.positive
def test_reorder_tracks_with_minimal_params_should_return_200(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        range_start=0,
        insert_before=1
    )
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Reorder tracks with minimal params")


@pytest.mark.positive
def test_reorder_tracks_with_range_length_should_return_200(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        range_start=0,
        insert_before=2,
        range_length=1
    )
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Reorder tracks with range_length")


@pytest.mark.negative
def test_replace_tracks_with_invalid_uri_should_return_400(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        uris=["spotify:track:INVALID"]
    )
    assert_error_response(response, expected_status=400, expected_message_substring="invalid")


@pytest.mark.negative
def test_reorder_tracks_missing_insert_before_should_return_400(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        range_start=1
        # missing insert_before
    )
    assert_error_response(response, expected_status=400, expected_message_substring="Missing range_start parameter")


@pytest.mark.negative
def test_reorder_tracks_with_invalid_range_should_return_4xx(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        range_start=100,
        insert_before=1
    )
    assert_error_response(response, expected_status_codes=[400, 403], expected_message_substring="Tracks selected to "
                                                                                                 "be reordered are "
                                                                                                 "out of bounds")


@pytest.mark.negative
def test_reorder_tracks_without_auth_should_return_401(default_playlist_id, sample_uris):
    unauth_client = PlaylistClient(RequestHandler(token=""))
    response = unauth_client.reorder_or_replace_tracks(
        playlist_id=default_playlist_id,
        uris=sample_uris
    )
    assert_error_response(response, expected_status=400, expected_message_substring="Only valid bearer authentication "
                                                                                    "supported")
