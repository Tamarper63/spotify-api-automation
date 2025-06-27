import pytest
from infra.models.playlist_response import PlaylistResponse
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_response_schema,
    assert_error_response,
)


@pytest.mark.positive
def test_get_playlist_should_return_200(user_api_clients, default_playlist_id):
    response = user_api_clients.spotify.get_playlist(default_playlist_id)
    assert_status_code_ok(response, 200, "Get playlist")


@pytest.mark.positive
def test_get_playlist_model_schema(user_api_clients, default_playlist_id):
    response = user_api_clients.spotify.get_playlist(default_playlist_id)
    assert_status_code_ok(response, 200)
    assert_response_schema(response.json(), PlaylistResponse)


@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", ["invalid_id", "123", "!!!"])
def test_get_playlist_with_invalid_id_should_return_400(user_api_clients, invalid_id):
    response = user_api_clients.spotify.get_playlist(invalid_id)
    assert_error_response(
        response,
        expected_status_codes=400,
        expected_message_substring="invalid base62 id"
    )


@pytest.mark.negative
def test_get_playlist_with_market_param(user_api_clients, default_playlist_id):
    response = user_api_clients.spotify.get_playlist(default_playlist_id, market="US")
    assert_status_code_ok(response, 200)


@pytest.mark.negative
def test_get_playlist_with_fields_param(user_api_clients, default_playlist_id):
    response = user_api_clients.spotify.get_playlist(default_playlist_id, fields="name,id")
    assert_status_code_ok(response, 200)


@pytest.mark.negative
def test_get_playlist_with_nested_fields_param(user_api_clients, default_playlist_id):
    response = user_api_clients.spotify.get_playlist(default_playlist_id, fields="tracks.items(track(name,href))")
    assert_status_code_ok(response, 200)


@pytest.mark.negative
def test_get_playlist_with_additional_types(user_api_clients, default_playlist_id):
    response = user_api_clients.spotify.get_playlist(default_playlist_id, additional_types="track")
    assert_status_code_ok(response, 200)


@pytest.mark.negative
def test_get_playlist_with_all_params(user_api_clients, default_playlist_id):
    response = user_api_clients.spotify.get_playlist(
        default_playlist_id,
        market="US",
        fields="name",
        additional_types="track"
    )
    assert_status_code_ok(response, 200)


@pytest.mark.negative
def test_get_playlist_with_empty_id(user_api_clients):
    response = user_api_clients.spotify.get_playlist("")
    assert_error_response(
        response,
        expected_status_codes=[400, 404]
    )
