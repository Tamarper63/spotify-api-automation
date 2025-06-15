# tests/playlists/test_create_playlist.py

import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_keys_exist,
    assert_json_field_equals
)

VALID_USER_ID = "spotify"


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize("name, public, description", [
    ("API Created Playlist", True, "Playlist created for automation test"),
])
def test_create_playlist_success(user_api_clients, name, public, description):
    user_response = user_api_clients.user.get_current_user_profile()
    user_id = user_response.json()["id"]

    response = user_api_clients.playlist.create_playlist(
        user_id,
        name=name,
        public=public,
        description=description
    )

    assert_status_code_ok(response, 201, "Create playlist success")
    response_json = response.json()
    assert_keys_exist(response_json, ["id", "name", "public", "description"])
    assert_json_field_equals(response, "name", name, "Name check")
    assert_json_field_equals(response, "description", description, "Description check")
    assert_json_field_equals(response, "public", public, "Public status check")


@pytest.mark.negative
def test_create_playlist_missing_name(api_clients):
    response = api_clients.playlist.create_playlist(VALID_USER_ID, name="")
    assert response.status_code in [401], f"Unexpected status: {response.status_code}"


@pytest.mark.negative
@pytest.mark.parametrize("invalid_user_id, expected_status", [
    ("invalid_user_123", 403),
    ("", 400),
    (None, 403),
])
def test_create_playlist_invalid_user(user_api_clients, invalid_user_id, expected_status):
    response = user_api_clients.playlist.create_playlist(invalid_user_id, name="Test Playlist")
    assert response.status_code == expected_status, (
        f"❌ Expected {expected_status}, got {response.status_code}. "
        f"Response: {response.text}"
    )


@pytest.mark.negative
def test_create_playlist_missing_token():
    from infra.http.request_handler import RequestHandler
    from infra.api_clients.playlist_client import PlaylistClient

    handler = RequestHandler(token="")
    client = PlaylistClient(handler)
    response = client.create_playlist(VALID_USER_ID, name="No Token Playlist")
    assert response.status_code in [400]


@pytest.mark.contract
def test_create_playlist_response_contract(user_api_clients):
    user_response = user_api_clients.user.get_current_user_profile()
    user_id = user_response.json()["id"]

    response = user_api_clients.playlist.create_playlist(
        user_id,
        name="Contract Check Playlist"
    )

    assert_status_code_ok(response, 201)
    expected_keys = {
        "id", "name", "public", "description", "external_urls",
        "href", "owner", "tracks", "type", "uri"
    }
    assert_keys_exist(response.json(), expected_keys)
