
import pytest
import time
import requests

from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response,
)


@pytest.fixture
def new_temp_playlist(spotify_user_client):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    playlist_name = f"Temp_{int(time.time())}"
    playlist_id = spotify_user_client.create_playlist(user_id, playlist_name).json()["id"]
    yield playlist_id
    spotify_user_client.unfollow_playlist(playlist_id)


@pytest.fixture
def followed_playlist(spotify_user_client, new_temp_playlist):
    spotify_user_client.follow_playlist(new_temp_playlist)
    return new_temp_playlist


# ===========================
# Positive Tests
# ===========================

@pytest.mark.positive
@pytest.mark.parametrize("name, public, collaborative, description", [
    ("Automation Playlist", True, False, "Updated via automation test"),
    ("Private Playlist", False, False, "Private & non-collab"),
    ("Name only update", None, None, None),
    (None, None, None, "Only description changed"),
    ("Set to private", False, None, "Making private")
])
def test_change_playlist_details_optional_params_should_return_200(
    spotify_user_client, followed_playlist, name, public, collaborative, description
):
    response = spotify_user_client.change_playlist_details(
        playlist_id=followed_playlist,
        name=name,
        public=public,
        collaborative=collaborative,
        description=description
    )
    if response.status_code == 502:
        pytest.skip("Spotify API returned 502 — unstable")
    assert_status_code_ok(response, 200, "Change playlist details with optional params")


# ===========================
# Behavioral Test
# ===========================

@pytest.mark.behavior
def test_public_update_succeeds_even_without_follow(spotify_user_client, new_temp_playlist):
    response = spotify_user_client.change_playlist_details(
        playlist_id=new_temp_playlist,
        public=True
    )
    assert_status_code_ok(response, 200, "Spotify allows making playlist public without follow")


# ===========================
# Negative Tests
# ===========================

@pytest.mark.negative
def test_change_playlist_public_and_collaborative_should_return_403(spotify_user_client, followed_playlist):
    response = spotify_user_client.change_playlist_details(
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
def test_change_playlist_with_empty_name_should_not_change_name(spotify_user_client, followed_playlist):
    original_playlist = spotify_user_client.get_playlist(followed_playlist).json()
    original_name = original_playlist["name"]

    response = spotify_user_client.change_playlist_details(
        playlist_id=followed_playlist,
        name=""
    )
    assert_status_code_ok(response, 200, "Change playlist details with empty name")

    updated_playlist = spotify_user_client.get_playlist(followed_playlist).json()
    assert updated_playlist["name"] == original_name, "❌ Playlist name should not change on empty update"



@pytest.mark.negative
def test_change_playlist_with_long_description_should_return_400(spotify_user_client, followed_playlist):
    long_description = "A" * 1001
    response = spotify_user_client.change_playlist_details(
        playlist_id=followed_playlist,
        description=long_description
    )
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="description"
    )


@pytest.mark.negative
def test_change_playlist_without_auth_should_return_400(unauthenticated_playlist_client, default_playlist_id):
    response = unauthenticated_playlist_client.change_playlist_details(
        playlist_id=default_playlist_id,
        name="Should Fail"
    )
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="Only valid bearer"
    )


@pytest.mark.negative
def test_change_playlist_with_invalid_id_should_return_404(spotify_user_client):
    response = spotify_user_client.change_playlist_details(
        playlist_id="nonexistent123",
        name="Should Fail"
    )
    assert_error_response(
        response,
        expected_status_codes=[400, 404],
        expected_message_substring="invalid"
    )
