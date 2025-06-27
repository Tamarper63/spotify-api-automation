import pytest
from utils.assertion_manager import assert_status_code_ok, assert_error_response
from infra.http.request_handler import RequestHandler
from infra.api_clients.spotify_client import SpotifyClient

@pytest.mark.contract
@pytest.mark.integration
@pytest.mark.parametrize("public", [True, False])
def test_follow_playlist_ok(spotify_user_client, default_playlist_id, public):
    response = spotify_user_client.follow_playlist(default_playlist_id, public=public)
    assert_status_code_ok(response, 200)

@pytest.mark.contract
@pytest.mark.integration
def test_unfollow_playlist_ok(spotify_user_client, default_playlist_id):
    response = spotify_user_client.unfollow_playlist(default_playlist_id)
    assert_status_code_ok(response, 200)

@pytest.mark.negative
def test_follow_playlist_invalid_token(default_playlist_id):
    handler = RequestHandler(token="INVALID")
    client = SpotifyClient(handler)
    response = client.follow_playlist(default_playlist_id, public=True)
    assert_error_response(response, expected_status_codes=401)

@pytest.mark.negative
def test_follow_playlist_invalid_id(spotify_user_client):
    response = spotify_user_client.follow_playlist("invalid123", public=True)
    assert response.status_code in (400, 404)

@pytest.mark.negative
def test_unfollow_playlist_invalid_token(default_playlist_id):
    handler = RequestHandler(token="INVALID")
    client = SpotifyClient(handler)
    response = client.unfollow_playlist(default_playlist_id)
    assert_error_response(response, expected_status_codes=401)

@pytest.mark.negative
def test_unfollow_playlist_invalid_id(spotify_user_client):
    response = spotify_user_client.unfollow_playlist("invalid123")
    assert response.status_code in (400, 404)

@pytest.mark.behavior
def test_unfollow_playlist_idempotent(spotify_user_client, default_playlist_id):
    response1 = spotify_user_client.unfollow_playlist(default_playlist_id)
    response2 = spotify_user_client.unfollow_playlist(default_playlist_id)
    assert_status_code_ok(response1, 200)
    assert_status_code_ok(response2, 200)
