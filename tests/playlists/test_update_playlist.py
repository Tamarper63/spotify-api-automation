import pytest

from tests.constants.auth_constants import DEFAULT_STATUS_OK
from tests.constants.playlist_constants import PLAYLIST_ITEMS_OPTIONAL_PARAMS_FILE
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_playlist_items_response_keys_exist,
    assert_playlist_items_schema,
    assert_playlist_items_with_limit,
)
from utils.yaml_loader import load_yaml_data


@pytest.mark.contract
def test_get_playlist_items_contract(user_api_clients, default_playlist_id):
    response = user_api_clients.spotify.get_playlist_items(default_playlist_id)
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Get playlist items contract")
    assert_playlist_items_response_keys_exist(response)


@pytest.mark.positive
@pytest.mark.parametrize("params", load_yaml_data(PLAYLIST_ITEMS_OPTIONAL_PARAMS_FILE)["optional_params"])
def test_get_playlist_items_with_optional_params(user_api_clients, default_playlist_id, params):
    response = user_api_clients.spotify.get_playlist_items(
        playlist_id=default_playlist_id,
        market=params["market"],
        limit=params["limit"],
        offset=params["offset"]
    )
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Get playlist items with optional params")
    assert_playlist_items_response_keys_exist(response)


@pytest.mark.contract
def test_get_playlist_items_model_schema(user_api_clients, default_playlist_id):
    response = user_api_clients.spotify.get_playlist_items(default_playlist_id)
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Validate playlist items schema")
    assert_playlist_items_schema(response)


@pytest.mark.positive
@pytest.mark.parametrize("params", load_yaml_data(PLAYLIST_ITEMS_OPTIONAL_PARAMS_FILE)["optional_params"])
def test_get_playlist_items_limit_match_response(user_api_clients, default_playlist_id, params):
    response = user_api_clients.spotify.get_playlist_items(
        playlist_id=default_playlist_id,
        market=params["market"],
        limit=params["limit"],
        offset=params["offset"]
    )
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Validate limit in response")
    assert_playlist_items_with_limit(response, params["limit"])
