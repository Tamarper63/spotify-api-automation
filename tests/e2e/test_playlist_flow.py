import pytest

from tests.helpers.e2e_flows import (
    create_test_playlist,
    get_user_id,
    add_and_verify_tracks,
    update_playlist_and_verify,
    validate_playlist_items,
    remove_and_reorder_track,
    cleanup_playlist,
)

TRACKS = [
    "spotify:track:4iV5W9uYEdYUVa79Axb7Rh",  # Daft Punk
    "spotify:track:1301WleyT98MSxVHPZCA6M",  # Arctic Monkeys
]


@pytest.mark.e2e
def test_full_playlist_lifecycle_flow(spotify_user_client):
    user_id = get_user_id(spotify_user_client)
    playlist_id = create_test_playlist(spotify_user_client, user_id)

    try:
        add_and_verify_tracks(spotify_user_client, playlist_id, TRACKS)
        update_playlist_and_verify(
            spotify_user_client, playlist_id, new_name="updated_name"
        )
        validate_playlist_items(spotify_user_client, playlist_id)
        remove_and_reorder_track(spotify_user_client, playlist_id, TRACKS[0])
    finally:
        cleanup_playlist(spotify_user_client, playlist_id)
