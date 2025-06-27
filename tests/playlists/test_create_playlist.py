import pytest
import time
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_error_response,
)


@pytest.mark.positive
def test_create_playlist_should_return_201(user_api_clients):
    user_id = user_api_clients.user.get_current_user_profile().json()["id"]
    playlist_name = f"My New Playlist {int(time.time())}"
    response = user_api_clients.playlist.create_playlist(user_id, playlist_name)
    assert_status_code_ok(response, 201, "Create playlist")


@pytest.mark.positive
@pytest.mark.parametrize("public, collaborative", [
    (True, False),
    (False, False),
    (False, True),
])
def test_create_playlist_optional_fields(user_api_clients, public, collaborative):
    user_id = user_api_clients.user.get_current_user_profile().json()["id"]
    playlist_name = f"Param Playlist {int(time.time())}"
    response = user_api_clients.playlist.create_playlist(
        user_id, playlist_name, public=public, collaborative=collaborative
    )
    assert_status_code_ok(response, 201, "Create playlist with optional flags")


@pytest.mark.negative
def test_create_playlist_missing_name(user_api_clients):
    user_id = user_api_clients.user.get_current_user_profile().json()["id"]
    response = user_api_clients.playlist.create_playlist(user_id, name=None)
    assert_error_response(response, expected_status_codes=400)


@pytest.mark.negative
def test_create_playlist_missing_token(default_playlist_id):
    import requests

    payload = {
        "name": f"No Token Playlist {int(time.time())}",
        "public": False,
        "description": "Should fail"
    }

    url = f"https://api.spotify.com/v1/users/fake_user_id/playlists"
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload
    )
    assert_error_response(response, expected_status_codes=401)
