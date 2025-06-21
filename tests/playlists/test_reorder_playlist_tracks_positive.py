import pytest
from utils.assertion_manager import assert_status_code_ok


@pytest.mark.positive
def test_reorder_valid_tracks_should_return_200(user_api_clients, reorder_ready_playlist):
    response = user_api_clients.playlist.reorder_playlist_items(
        playlist_id=reorder_ready_playlist,
        range_start=0,
        insert_before=1
    )
    assert_status_code_ok(response, 200, "Reorder tracks in playlist")
