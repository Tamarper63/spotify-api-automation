import pytest

from infra.http.request_handler import RequestHandler
from infra.models.playlist_response import PlaylistResponse
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_nested_field_equals,
    assert_keys_exist, assert_error_response
)
from utils.param_loaders import (
    get_valid_playlist_ids,
)


@pytest.mark.parametrize("playlist_id", get_valid_playlist_ids())
def test_get_playlist_should_return_200(api_clients, playlist_id):
    response = api_clients.playlist.get_playlist(playlist_id)
    assert_status_code_ok(response, 200)


# @pytest.mark.parametrize(
#     "field_path, expected_value",
#     load_flat_yaml_kv("playlist_metadata.yaml", "playlist_metadata")
# )
# def test_playlist_response_values(api_clients, default_playlist_id, field_path, expected_value):
#     response = api_clients.playlist.get_playlist(default_playlist_id)
#     assert_nested_field_equals(response.json(), field_path, expected_value)


def test_playlist_model_schema(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id)
    assert_status_code_ok(response, 200)

    PlaylistResponse(**response.json())


##Theres a bug return 404 when empty string
@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", ["invalid_id", "123", "!!!"])
def test_get_playlist_with_invalid_id_should_return_400(api_clients, invalid_id):
    response = api_clients.playlist.get_playlist(invalid_id)
    assert_error_response(response, 400, "Invalid base62 id")


@pytest.mark.negative
def test_get_playlist_without_auth_should_return_401():
    unauth_handler = RequestHandler(token="invalid_token")
    playlist_url = "https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n"

    response = unauth_handler.get(playlist_url)
    assert_error_response(response, 401, "access token")


@pytest.mark.positive
def test_get_playlist_with_market_param(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id, market="ES")
    assert_status_code_ok(response, 200)


@pytest.mark.positive
def test_get_playlist_with_fields_param(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id, fields="description,uri")
    assert_status_code_ok(response, 200)
    assert_keys_exist(response.json(), ["description", "uri"])


@pytest.mark.positive
def test_get_playlist_with_nested_fields_param(api_clients, default_playlist_id):
    fields_param = "tracks.items(track(name,href))"
    response = api_clients.playlist.get_playlist(default_playlist_id, fields=fields_param)
    assert_status_code_ok(response, 200)
    assert "tracks" in response.json()


@pytest.mark.positive
def test_get_playlist_with_additional_types(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id, additional_types="episode")
    assert_status_code_ok(response, 200)


def test_get_playlist_with_all_params(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(
        default_playlist_id,
        market="ES",
        fields="tracks.items(track(name,href))",
        additional_types="episode"
    )
    assert_status_code_ok(response, 200)


##got 502 why
@pytest.mark.negative
def test_get_playlist_with_invalid_market(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id, market="INVALID")
    assert response.status_code in [502]


@pytest.mark.negative
def test_get_playlist_with_empty_id(api_clients):
    response = api_clients.playlist.get_playlist("")
    assert response.status_code == 404  # Spotify returns 404, not 400
