import pytest

from infra.api_clients.spotify_client import SpotifyClient
from infra.config.settings import get_settings
from infra.http.request_handler import RequestHandler
from tests.playlists.track_fixtures import sample_uris, invalid_track_uri


@pytest.fixture
def unauthenticated_playlist_client():
    return SpotifyClient(RequestHandler(token=""))


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="session")
def default_playlist_id(settings) -> str:
    return settings.default_playlist_id


@pytest.fixture
def isolated_test_playlist(spotify_user_client, sample_uris):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    playlist_id = spotify_user_client.create_playlist(user_id=user_id, name="Isolated Playlist").json()["id"]
    spotify_user_client.add_tracks_to_playlist(playlist_id, sample_uris)
    yield playlist_id
    spotify_user_client.unfollow_playlist(playlist_id)


@pytest.fixture
def reorder_ready_playlist(spotify_user_client, sample_uris):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    playlist_id = spotify_user_client.create_playlist(user_id, name="Reorder Ready Playlist").json()["id"]
    spotify_user_client.add_tracks_to_playlist(playlist_id, sample_uris)
    yield playlist_id
    spotify_user_client.unfollow_playlist(playlist_id)
