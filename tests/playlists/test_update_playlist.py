import pytest
from tests.constants.auth_constants import DEFAULT_STATUS_OK
from tests.constants.playlist_constants import PLAYLIST_ITEMS_OPTIONAL_PARAMS_FILE
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_playlist_items_response_keys_exist,
    assert_playlist_items_schema,
)
from utils.yaml_loader import load_yaml_data


@pytest.mark.contract
def test_get_playlist_items_contract(spotify_user_client, default_playlist_id):
    response = spotify_user_client.get_playlist_items(default_playlist_id)
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Get playlist items contract")
    assert_playlist_items_response_keys_exist(response)


@pytest.mark.positive
@pytest.mark.parametrize(
    "params", load_yaml_data(PLAYLIST_ITEMS_OPTIONAL_PARAMS_FILE)["optional_params"]
)
def test_get_playlist_items_with_optional_params(
    spotify_user_client, default_playlist_id, params
):
    response = spotify_user_client.get_playlist_items(
        playlist_id=default_playlist_id,
        market=params.get("market"),
        limit=params.get("limit"),
        offset=params.get("offset"),
    )
    assert_status_code_ok(
        response, DEFAULT_STATUS_OK, "Get playlist items with optional params"
    )
    assert_playlist_items_response_keys_exist(response)


@pytest.mark.contract
def test_get_playlist_items_model_schema(spotify_user_client, default_playlist_id):
    response = spotify_user_client.get_playlist_items(default_playlist_id)
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Validate playlist items schema")
    assert_playlist_items_schema(response)


@pytest.mark.positive
@pytest.mark.parametrize(
    "params", load_yaml_data(PLAYLIST_ITEMS_OPTIONAL_PARAMS_FILE)["optional_params"]
)
def test_get_playlist_items_limit_match_response(
    spotify_user_client, default_playlist_id, params
):
    response = spotify_user_client.get_playlist_items(
        playlist_id=default_playlist_id,
        market=params.get("market"),
        limit=params.get("limit"),
        offset=params.get("offset"),
    )
    assert_status_code_ok(response, DEFAULT_STATUS_OK, "Validate limit in response")

    actual_limit = response.json().get("limit")
    items_count = len(response.json().get("items", []))

    assert actual_limit is not None, "❌ No limit field in response"
    assert (
        items_count <= params["limit"]
    ), f"❌ Expected at most {params['limit']} items, but got {items_count}"
