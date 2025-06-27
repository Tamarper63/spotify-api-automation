from unittest import skip
import pytest


@skip
@pytest.mark.positive
def test_full_playlist_lifecycle(user_api_clients, sample_uris):
    response_create = user_api_clients.spotify.create_playlist(
        user_id=user_api_clients.spotify.get_current_user_profile().json()["id"],
        name="E2E Test Playlist"
    )
    assert response_create.status_code == 201
    playlist_id = response_create.json()["id"]

    response_add = user_api_clients.spotify.add_tracks_to_playlist(
        playlist_id, uris=sample_uris
    )
    assert response_add.status_code == 201

    updated_name = "E2E Test Playlist (Updated)"
    response_change = user_api_clients.spotify.change_playlist_details(
        playlist_id=playlist_id,
        name=updated_name
    )
    assert response_change.status_code == 200

    response_get = user_api_clients.spotify.get_playlist(playlist_id)
    assert response_get.status_code == 200
    assert response_get.json()["name"] == updated_name

    response_remove = user_api_clients.spotify.remove_tracks_from_playlist(
        playlist_id, uris=sample_uris
    )
    assert response_remove.status_code == 200
