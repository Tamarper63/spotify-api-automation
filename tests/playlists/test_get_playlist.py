import pytest
from infra.models.playlist_response import PlaylistResponse
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_response_schema,
    assert_error_response,
)
from infra.http.request_handler import RequestHandler
from infra.api_clients.spotify_client import SpotifyClient


# === Positive Tests ===

@pytest.mark.positive
def test_get_playlist_should_return_200(spotify_user_client, default_playlist_id):
    response = spotify_user_client.get_playlist(default_playlist_id)
    assert_status_code_ok(response, 200, "Get playlist")


@pytest.mark.positive
def test_get_playlist_model_schema(spotify_user_client, default_playlist_id):
    response = spotify_user_client.get_playlist(default_playlist_id)
    assert_status_code_ok(response, 200)
    assert_response_schema(response.json(), PlaylistResponse)


@pytest.mark.positive
@pytest.mark.parametrize("market", ["US", "IL"])
def test_get_playlist_with_market_param(spotify_user_client, default_playlist_id, market):
    response = spotify_user_client.get_playlist(default_playlist_id, market=market)
    assert_status_code_ok(response, 200)


@pytest.mark.positive
@pytest.mark.parametrize("fields", ["name,id", "tracks.items(track(name,href))"])
def test_get_playlist_with_fields_param(spotify_user_client, default_playlist_id, fields):
    response = spotify_user_client.get_playlist(default_playlist_id, fields=fields)
    assert_status_code_ok(response, 200)


@pytest.mark.positive
def test_get_playlist_with_additional_types(spotify_user_client, default_playlist_id):
    response = spotify_user_client.get_playlist(default_playlist_id, additional_types="track")
    assert_status_code_ok(response, 200)


@pytest.mark.positive
def test_get_playlist_with_all_params(spotify_user_client, default_playlist_id):
    response = spotify_user_client.get_playlist(
        default_playlist_id,
        market="US",
        fields="name",
        additional_types="track"
    )
    assert_status_code_ok(response, 200)


# === Negative Tests ===

@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", ["invalid_id", "123", "!!!"])
def test_get_playlist_with_invalid_id_should_return_400(spotify_user_client, invalid_id):
    response = spotify_user_client.get_playlist(invalid_id)
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="invalid base62 id"
    )


@pytest.mark.negative
def test_get_playlist_with_empty_id(spotify_user_client):
    response = spotify_user_client.get_playlist("")
    assert_error_response(response, expected_status_codes=[400, 404])


@pytest.mark.negative
def test_get_playlist_invalid_token(default_playlist_id):
    handler = RequestHandler(token="INVALID")
    client = SpotifyClient(handler)
    response = client.get_playlist(default_playlist_id)
    assert_error_response(response, expected_status_codes=401, expected_message_substring="Invalid access token")


@pytest.mark.negative
def test_get_playlist_nonexistent_playlist_should_return_404(spotify_user_client):
    valid_but_fake_id = "3cEyTGIE0p9zb5Fr" + "XYZ123"  # 22-char base62-like ID
    response = spotify_user_client.get_playlist(valid_but_fake_id)
    assert_error_response(response, expected_status_codes=404, expected_message_substring="Not found")
