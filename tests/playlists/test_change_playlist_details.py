import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response
)


@pytest.mark.positive
@pytest.mark.parametrize("name, public, collaborative, description", [
    ("Automation Playlist", True, False, "Updated via automation test"),
    ("Private Playlist", False, False, "Private & non-collab"),
    ("Name only update", None, None, None),
    (None, None, None, "Only description changed"),
    ("Set to private", False, None, "Making private")
])
def test_change_playlist_details_optional_params_should_return_200(
    user_api_clients, default_playlist_id, name, public, collaborative, description
):
    response = user_api_clients.playlist.change_playlist_details(
        playlist_id=default_playlist_id,
        name=name,
        public=public,
        collaborative=collaborative,
        description=description
    )
    assert_status_code_ok(response, 200, "Change playlist details with optional params")


@pytest.mark.negative
def test_change_playlist_invalid_id_should_return_400(user_api_clients):
    response = user_api_clients.playlist.change_playlist_details(
        playlist_id="invalid_playlist_123",
        name="Invalid ID Test"
    )
    assert_error_response(response, expected_status=400)


@pytest.mark.negative
def test_change_playlist_without_auth(unauthenticated_playlist_client, default_playlist_id):
    response = unauthenticated_playlist_client.change_playlist_details(
        playlist_id=default_playlist_id,
        name="Unauth test"
    )
    assert_error_response(response, expected_status=400)


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
        expected_status=403,
        expected_message_substring="public playlists collaborative"
    )
