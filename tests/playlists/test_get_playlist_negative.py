import pytest

from infra.http.request_handler import RequestHandler
from infra.models.playlist_response import PlaylistResponse
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_nested_field_equals,
    assert_keys_exist,
    assert_error_response,
)
from utils.param_loaders import get_valid_playlist_ids
from tests.constants.playlist_constants import (
    INVALID_PLAYLIST_IDS,
    INVALID_MARKET,
    VALID_MARKET,
    SIMPLE_FIELDS,
    NESTED_FIELDS,
    ADDITIONAL_TYPES,
    DEFAULT_PLAYLIST_URL,
)


@pytest.mark.positive
@pytest.mark.parametrize("playlist_id", get_valid_playlist_ids())
def test_get_playlist_should_return_200(api_clients, playlist_id):
    response = api_clients.playlist.get_playlist(playlist_id)
    assert_status_code_ok(response, 200)


@pytest.mark.contract
def test_get_playlist_model_schema(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id)
    assert_status_code_ok(response, 200)
    PlaylistResponse(**response.json())  # model-based contract


@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", INVALID_PLAYLIST_IDS)
def test_get_playlist_with_invalid_id_should_return_400(api_clients, invalid_id):
    response = api_clients.playlist.get_playlist(invalid_id)
    assert_error_response(response, expected_status_codes=400, expected_message_substring="Invalid base62 id")


@pytest.mark.negative
def test_get_playlist_without_auth_should_return_401():
    unauth_handler = RequestHandler(token="invalid_token")
    response = unauth_handler.get(DEFAULT_PLAYLIST_URL)
    assert_error_response(response, expected_status_codes=401, expected_message_substring="access token")


@pytest.mark.positive
def test_get_playlist_with_market_param(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id, market=VALID_MARKET)
    assert_status_code_ok(response, 200)


@pytest.mark.positive
def test_get_playlist_with_fields_param(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id, fields=SIMPLE_FIELDS)
    assert_status_code_ok(response, 200)
    assert_keys_exist(response.json(), ["description", "uri"])


@pytest.mark.positive
def test_get_playlist_with_nested_fields_param(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id, fields=NESTED_FIELDS)
    assert_status_code_ok(response, 200)
    assert "tracks" in response.json()


@pytest.mark.positive
def test_get_playlist_with_additional_types(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id, additional_types=ADDITIONAL_TYPES)
    assert_status_code_ok(response, 200)


@pytest.mark.positive
def test_get_playlist_with_all_params(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(
        default_playlist_id,
        market=VALID_MARKET,
        fields=NESTED_FIELDS,
        additional_types=ADDITIONAL_TYPES
    )
    assert_status_code_ok(response, 200)


@pytest.mark.negative
def test_get_playlist_with_invalid_market(api_clients, default_playlist_id):
    response = api_clients.playlist.get_playlist(default_playlist_id, market=INVALID_MARKET)
    assert_error_response(response, expected_status_codes=502)


@pytest.mark.negative
def test_get_playlist_with_empty_id(api_clients):
    response = api_clients.playlist.get_playlist("")
    assert_error_response(response, expected_status_codes=404)
