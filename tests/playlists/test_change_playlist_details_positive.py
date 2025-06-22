import pytest
from utils.assertion_manager import assert_status_code_ok


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
