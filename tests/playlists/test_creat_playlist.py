import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_keys_exist,
    assert_json_field_equals,
    assert_error_response
)
from tests.constants.playlist_constants import (
    DEFAULT_PLAYLIST_NAME,
    DEFAULT_DESCRIPTION,
    CONTRACT_PLAYLIST_NAME,
    MISSING_NAME_PLAYLIST,
    NO_TOKEN_PLAYLIST_NAME,
    VALID_USER_ID,
    INVALID_USER_ID_CASES,
    CREATE_PLAYLIST_KEYS
)


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize("name, public, description", [
    (DEFAULT_PLAYLIST_NAME, True, DEFAULT_DESCRIPTION),
])
def test_create_playlist_success(user_api_clients, name, public, description):
    user_id = user_api_clients.user.get_current_user_profile().json()["id"]

    response = user_api_clients.playlist.create_playlist(
        user_id=user_id,
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
    response = api_clients.playlist.create_playlist(VALID_USER_ID, name=MISSING_NAME_PLAYLIST)
    assert_error_response(response, expected_status=401)


@pytest.mark.negative
@pytest.mark.parametrize("invalid_user_id, expected_status", INVALID_USER_ID_CASES)
def test_create_playlist_invalid_user(user_api_clients, invalid_user_id, expected_status):
    response = user_api_clients.playlist.create_playlist(
        user_id=invalid_user_id,
        name="Test Playlist"
    )
    assert_error_response(response, expected_status=expected_status)


@pytest.mark.negative
def test_create_playlist_missing_token(unauthenticated_playlist_client):
    response = unauthenticated_playlist_client.create_playlist(
        user_id=VALID_USER_ID,
        name=NO_TOKEN_PLAYLIST_NAME
    )
    assert_error_response(response, expected_status=400)


@pytest.mark.contract
def test_create_playlist_response_contract(user_api_clients):
    user_id = user_api_clients.user.get_current_user_profile().json()["id"]

    response = user_api_clients.playlist.create_playlist(
        user_id=user_id,
        name=CONTRACT_PLAYLIST_NAME
    )

    assert_status_code_ok(response, 201, "Create playlist contract")
    assert_keys_exist(response.json(), CREATE_PLAYLIST_KEYS)
