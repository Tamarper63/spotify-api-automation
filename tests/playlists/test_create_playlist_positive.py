import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_keys_exist,
    assert_json_field_equals,
)
from tests.constants.playlist_constants import (
    DEFAULT_PLAYLIST_NAME,
    DEFAULT_DESCRIPTION,
    CREATE_PLAYLIST_KEYS,
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
