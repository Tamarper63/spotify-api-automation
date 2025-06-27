import pytest
import time
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_keys_exist
)

TRACKS = [
    "spotify:track:4iV5W9uYEdYUVa79Axb7Rh",  # Daft Punk
    "spotify:track:1301WleyT98MSxVHPZCA6M"   # Arctic Monkeys
]


@pytest.mark.e2e
def test_full_playlist_lifecycle_flow(spotify_user_client):
    # 1. Get user ID
    user_profile = spotify_user_client.get_current_user_profile()
    assert_status_code_ok(user_profile, 200, "Fetch current user profile")
    user_id = user_profile.json()["id"]

    # 2. Create new playlist
    playlist_name = f"e2e_{int(time.time())}"
    create_resp = spotify_user_client.create_playlist(
        user_id=user_id,
        name=playlist_name,
        public=False,
        collaborative=False,
        description="e2e test flow"
    )
    assert_status_code_ok(create_resp, 201, "Create playlist")
    playlist_id = create_resp.json()["id"]

    try:
        # 3. Add tracks
        add_resp = spotify_user_client.add_tracks_to_playlist(playlist_id, uris=TRACKS)
        assert_status_code_ok(add_resp, 201, "Add tracks to playlist")

        # 4. Update playlist metadata
        update_resp = spotify_user_client.change_playlist_details(
            playlist_id, name=f"{playlist_name}_updated", public=True
        )
        assert_status_code_ok(update_resp, 200, "Update playlist details")

        # 5. Get playlist items
        items_resp = spotify_user_client.get_playlist_items(playlist_id, limit=2)
        assert_status_code_ok(items_resp, 200, "Fetch playlist items")
        assert_keys_exist(items_resp.json(), ["items", "limit", "href"])

        # 6. Remove track
        remove_resp = spotify_user_client.remove_tracks_from_playlist(
            playlist_id, uris=[TRACKS[0]]
        )
        assert_status_code_ok(remove_resp, 200, "Remove track")

        # 7. Reorder remaining track (noop if only one)
        reorder_resp = spotify_user_client.reorder_playlist_items(
            playlist_id, range_start=0, insert_before=0
        )
        assert_status_code_ok(reorder_resp, 200, "Reorder playlist (noop)")

    finally:
        # 8. Cleanup: unfollow (delete)
        cleanup_resp = spotify_user_client.unfollow_playlist(playlist_id)
        assert_status_code_ok(cleanup_resp, 200, "Unfollow/delete playlist")
