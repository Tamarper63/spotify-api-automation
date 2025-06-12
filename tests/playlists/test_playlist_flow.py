import pytest

from infra.assertions.assertion_manager import assert_status_code_ok, assert_keys_exist
from utils.yaml_loader import load_yaml_data


@pytest.mark.smoke
def test_create_playlist_should_return_201(api_clients):
    user_id = "test_user_id"
    response = api_clients.playlist.create_playlist(user_id=user_id, name="My Playlist")
    assert response.status_code == 201
    assert "id" in response.json()


def test_add_tracks_should_return_201(api_clients):
    playlist_id = "some_id"
    uris = ["spotify:track:1", "spotify:track:2"]
    response = api_clients.playlist.add_tracks(playlist_id, uris)
    assert response.status_code == 201


@pytest.mark.parametrize("playlist", load_yaml_data("playlist_ids.yaml")["valid_playlists"])
@pytest.mark.smoke
def test_get_playlist_should_return_200(api_clients, playlist):
    response = api_clients.playlist.get_playlist(playlist["id"])
    assert_status_code_ok(response, 200, f"GET /playlists/{playlist['id']}")
    assert_keys_exist(response.json(), ["id", "name", "tracks"])
    assert response.json()["name"] == playlist["expected_name"]
