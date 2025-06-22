import pytest
from utils.assertion_manager import assert_error_response
from tests.constants.playlist_constants import INVALID_PLAYLIST_IDS


@pytest.mark.negative
@pytest.mark.parametrize("playlist_id, expected_status", [
    ("invalid_id", 400),
    ("", 400),  # or another status based on API behavior
])
def test_get_playlist_items_invalid_id_should_fail(user_api_clients, playlist_id, expected_status):
    response = user_api_clients.playlist.get_playlist_items(playlist_id)
    assert_error_response(response, expected_status_codes=expected_status, expected_message_substring="Invalid")
