import pytest
from utils.assertion_manager import assert_error_response
from tests.constants.playlist_constants import (
    MISSING_NAME_PLAYLIST,
    NO_TOKEN_PLAYLIST_NAME,
    VALID_USER_ID,
    INVALID_USER_ID_CASES,
)


@pytest.mark.negative
def test_create_playlist_missing_name(api_clients):
    response = api_clients.playlist.create_playlist(
        VALID_USER_ID,
        name=MISSING_NAME_PLAYLIST
    )
    assert_error_response(response, expected_status_codes=401)


@pytest.mark.negative
@pytest.mark.parametrize("invalid_user_id, expected_status", INVALID_USER_ID_CASES)
def test_create_playlist_invalid_user(user_api_clients, invalid_user_id, expected_status):
    response = user_api_clients.playlist.create_playlist(
        user_id=invalid_user_id,
        name="Test Playlist"
    )
    assert_error_response(response, expected_status_codes=expected_status)


@pytest.mark.negative
def test_create_playlist_missing_token(unauthenticated_playlist_client):
    response = unauthenticated_playlist_client.create_playlist(
        user_id=VALID_USER_ID,
        name=NO_TOKEN_PLAYLIST_NAME
    )
    assert_error_response(response, expected_status_codes=400)
