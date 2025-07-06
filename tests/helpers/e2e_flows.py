import time
from utils.assertion_manager import assert_status_code_ok, assert_keys_exist


def get_user_id(client):
    user_profile = client.get_current_user_profile()
    assert_status_code_ok(user_profile, 200, "Fetch current user profile")
    return user_profile.json()["id"]


def create_test_playlist(client, user_id: str, name_prefix="e2e") -> str:
    playlist_name = f"{name_prefix}_{int(time.time())}"
    response = client.create_playlist(
        user_id=user_id,
        name=playlist_name,
        public=False,
        collaborative=False,
        description="e2e test flow",
    )
    assert_status_code_ok(response, 201, "Create playlist")
    return response.json()["id"]


def add_and_verify_tracks(client, playlist_id: str, uris: list[str]):
    response = client.add_tracks_to_playlist(playlist_id, uris=uris)
    assert_status_code_ok(response, 201, "Add tracks to playlist")


def update_playlist_and_verify(client, playlist_id: str, new_name: str):
    response = client.change_playlist_details(playlist_id, name=new_name, public=True)
    assert_status_code_ok(response, 200, "Update playlist details")


def validate_playlist_items(client, playlist_id: str, limit=2):
    response = client.get_playlist_items(playlist_id, limit=limit)
    assert_status_code_ok(response, 200, "Fetch playlist items")
    assert_keys_exist(response.json(), ["items", "limit", "href"])


def remove_and_reorder_track(client, playlist_id: str, track_uri: str):
    remove_resp = client.remove_tracks_from_playlist(playlist_id, uris=[track_uri])
    assert_status_code_ok(remove_resp, 200, "Remove track")
    reorder_resp = client.reorder_playlist_items(
        playlist_id, range_start=0, insert_before=0
    )
    assert_status_code_ok(reorder_resp, 200, "Reorder playlist (noop)")


def cleanup_playlist(client, playlist_id: str):
    response = client.unfollow_playlist(playlist_id)
    assert_status_code_ok(response, 200, "Unfollow/delete playlist")
