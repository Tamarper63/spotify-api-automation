import pytest
import requests
import time

from infra.models.playlist_response import PlaylistResponse
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response,
    assert_response_schema,
)


@pytest.mark.positive
def test_create_playlist_should_return_201(spotify_user_client):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    playlist_name = f"My New Playlist {int(time.time())}"
    response = spotify_user_client.create_playlist(user_id, playlist_name)
    assert_status_code_ok(response, 201, "Create playlist")


@pytest.mark.positive
@pytest.mark.parametrize(
    "public, collaborative",
    [
        (True, False),
        (False, False),
        (False, True),
    ],
)
def test_create_playlist_optional_fields(spotify_user_client, public, collaborative):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    playlist_name = f"Param Playlist {int(time.time())}"
    response = spotify_user_client.create_playlist(
        user_id, playlist_name, public=public, collaborative=collaborative
    )
    assert_status_code_ok(response, 201, "Create playlist with optional flags")


@pytest.mark.negative
def test_create_playlist_missing_name(spotify_user_client):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    response = spotify_user_client.create_playlist(user_id, name=None)
    assert_error_response(response, expected_status_codes=400)


@pytest.mark.negative
def test_create_playlist_missing_token():
    payload = {
        "name": f"No Token Playlist {int(time.time())}",
        "public": False,
        "description": "Should fail",
    }
    url = f"https://api.spotify.com/v1/users/fake_user_id/playlists"
    response = requests.post(
        url, headers={"Content-Type": "application/json"}, json=payload
    )
    assert_error_response(response, expected_status_codes=401)


@pytest.mark.negative
def test_create_playlist_long_description_should_return_400(spotify_user_client):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    response = spotify_user_client.create_playlist(
        user_id=user_id, name="Long Description Playlist", description="A" * 1001
    )
    assert_error_response(
        response, expected_status_codes=400, expected_message_substring="description"
    )


@pytest.mark.positive
def test_create_playlist_long_name_should_return_201(spotify_user_client):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    long_name = "A" * 101
    response = spotify_user_client.create_playlist(user_id=user_id, name=long_name)
    assert_status_code_ok(response, 201, "Create playlist with long name")
    playlist = response.json()
    assert playlist["name"] == long_name, "Playlist name mismatch"


@pytest.mark.negative
def test_create_playlist_invalid_token_should_return_400(
    unauthenticated_playlist_client,
):
    fake_user_id = "fake_user_id"
    response = unauthenticated_playlist_client.create_playlist(
        user_id=fake_user_id, name="Invalid Token Test"
    )
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="Only valid bearer authentication supported",
    )


@pytest.mark.negative
def test_create_playlist_for_different_user_should_return_403(spotify_user_client):
    response = spotify_user_client.create_playlist(
        user_id="nonexistent_user_123", name="Another User Playlist"
    )
    assert_error_response(
        response,
        expected_status_codes=403,
        expected_message_substring="You cannot create a playlist for another user",
    )


@pytest.mark.positive
def test_create_playlist_schema_validation(spotify_user_client):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    response = spotify_user_client.create_playlist(user_id, "Schema Test")
    assert_status_code_ok(response, 201)
    assert_response_schema(response.json(), PlaylistResponse)
