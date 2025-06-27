import pytest
from utils.assertion_manager import assert_status_code_ok


@pytest.mark.contract
@pytest.mark.integration
@pytest.mark.parametrize("public", [True, False])
def test_follow_playlist_ok(user_api_clients, default_playlist_id, public):
    response = user_api_clients.playlist.follow_playlist(default_playlist_id, public=public)
    assert_status_code_ok(response, 200)


@pytest.mark.contract
@pytest.mark.integration
def test_unfollow_playlist_ok(user_api_clients, default_playlist_id):
    response = user_api_clients.playlist.unfollow_playlist(default_playlist_id)
    assert_status_code_ok(response, 200)


@pytest.mark.negative
def test_follow_playlist_invalid_token(default_playlist_id):
    from infra.http.request_handler import RequestHandler
    from infra.api_clients.playlist_client import PlaylistClient

    handler = RequestHandler(token="INVALID")
    client = PlaylistClient(handler)
    response = client.follow_playlist(default_playlist_id, public=True)
    assert response.status_code == 401


@pytest.mark.negative
def test_follow_playlist_invalid_id(user_api_clients):
    response = user_api_clients.playlist.follow_playlist("invalid123", public=True)
    assert response.status_code in (400, 404)
