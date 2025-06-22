import pytest
from utils.assertion_manager import assert_error_response


@pytest.mark.negative
def test_change_playlist_invalid_id_should_return_400(user_api_clients):
    response = user_api_clients.playlist.change_playlist_details(
        playlist_id="invalid_playlist_123",
        name="Invalid ID Test"
    )
    assert_error_response(response, expected_status_codes=400)


@pytest.mark.negative
def test_change_playlist_without_auth(unauthenticated_playlist_client, default_playlist_id):
    response = unauthenticated_playlist_client.change_playlist_details(
        playlist_id=default_playlist_id,
        name="Unauth test"
    )
    assert_error_response(response, expected_status_codes=400)


@pytest.mark.negative
def test_change_playlist_with_invalid_data(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.change_playlist_details(
        playlist_id=default_playlist_id,
        name=123456  # Invalid type (should be str)
    )
    assert_error_response(response, expected_status_codes=[400, 422, 500])


@pytest.mark.negative
def test_change_playlist_public_and_collaborative_should_return_403(user_api_clients, default_playlist_id):
    """
    According to Spotify API rules, a playlist cannot be both public and collaborative.
    """
    response = user_api_clients.playlist.change_playlist_details(
        playlist_id=default_playlist_id,
        public=True,
        collaborative=True
    )
    assert_error_response(
        response,
        expected_status_codes=403,
        expected_message_substring="public playlists collaborative"
    )
