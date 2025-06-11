import pytest


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


def test_get_playlist_should_return_200(api_clients):
    playlist_id = "some_id"
    response = api_clients.playlist.get_playlist(playlist_id)
    assert response.status_code == 200
    assert "name" in response.json()
