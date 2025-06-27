import pytest
import time

from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response,
)


@pytest.fixture
def new_temp_playlist(user_api_clients):
    user_id = user_api_clients.spotify.get_current_user_profile().json()["id"]
    playlist_name = f"Temp_{int(time.time())}"
    playlist_id = user_api_clients.spotify.create_playlist(user_id, playlist_name).json()["id"]
    yield playlist_id
    user_api_clients.spotify.unfollow_playlist(playlist_id)


@pytest.fixture
def followed_playlist(user_api_clients, new_temp_playlist):
    user_api_clients.spotify.follow_playlist(new_temp_playlist)
    return new_temp_playlist


@pytest.mark.positive
@pytest.mark.parametrize("name, public, collaborative, description", [
    ("Automation Playlist", True, False, "Updated via automation test"),
    ("Private Playlist", False, False, "Private & non-collab"),
    ("Name only update", None, None, None),
    (None, None, None, "Only description changed"),
    ("Set to private", False, None, "Making private")
])
def test_change_playlist_details_optional_params_should_return_200(
    user_api_clients, followed_playlist, name, public, collaborative, description
):
    response = user_api_clients.spotify.change_playlist_details(
        playlist_id=followed_playlist,
        name=name,
        public=public,
        collaborative=collaborative,
        description=description
    )
    if response.status_code == 502:
        pytest.skip("Spotify API returned 502 — unstable")
    assert_status_code_ok(response, 200, "Change playlist details with optional params")


@pytest.mark.negative
def test_change_playlist_public_and_collaborative_should_return_403(user_api_clients, followed_playlist):
    response = user_api_clients.spotify.change_playlist_details(
        playlist_id=followed_playlist,
        public=True,
        collaborative=True
    )
    assert_error_response(
        response,
        expected_status_codes=403,
        expected_message_substring="public playlists collaborative"
    )


@pytest.mark.behavior
def test_public_update_succeeds_even_without_follow(user_api_clients, new_temp_playlist):
    response = user_api_clients.spotify.change_playlist_details(
        playlist_id=new_temp_playlist,
        public=True
    )
    assert_status_code_ok(response, 200, "Spotify allows making playlist public without follow")
