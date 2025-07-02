import pytest
from infra.api_clients.spotify_client import SpotifyClient
from infra.http.request_handler import RequestHandler


@pytest.fixture
def unauthenticated_playlist_client():
    return SpotifyClient(RequestHandler(token=""))
