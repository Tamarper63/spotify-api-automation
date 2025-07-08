import pydantic_core
import pytest
from jsonschema import ValidationError

from infra.api_clients.spotify_client import SpotifyClient
from infra.config.loader import load_config
from infra.http.request_handler import RequestHandler
from tests.playlists.track_fixtures import sample_uris, invalid_track_uri


@pytest.fixture
def unauthenticated_playlist_client():
    return SpotifyClient(RequestHandler(token=""))


@pytest.fixture(scope="session")
def config():
    try:
        return load_config()
    except pydantic_core.ValidationError as e:
        print("🧨 MISSING CONFIG:", e.errors())
        raise



@pytest.fixture(scope="session")
def default_playlist_id(config) -> str:
    return config.default_playlist_id


@pytest.fixture
def isolated_test_playlist(spotify_user_client, sample_uris):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    playlist_id = spotify_user_client.create_playlist(
        user_id=user_id, name="Isolated Playlist"
    ).json()["id"]
    spotify_user_client.add_tracks_to_playlist(playlist_id, sample_uris)
    yield playlist_id
    spotify_user_client.unfollow_playlist(playlist_id)


@pytest.fixture
def reorder_ready_playlist(spotify_user_client, sample_uris):
    user_id = spotify_user_client.get_current_user_profile().json()["id"]
    playlist_id = spotify_user_client.create_playlist(
        user_id, name="Reorder Ready Playlist"
    ).json()["id"]
    spotify_user_client.add_tracks_to_playlist(playlist_id, sample_uris)
    yield playlist_id
    spotify_user_client.unfollow_playlist(playlist_id)
