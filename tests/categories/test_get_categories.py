# tests/browse/test_get_categories.py

import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_keys_exist,
    assert_error_response,
)
from infra.api_clients.spotify_client import SpotifyClient
from infra.http.request_handler import RequestHandler


# ===========================
# Positive / Contract
# ===========================

@pytest.mark.contract
@pytest.mark.integration
@pytest.mark.parametrize("locale, limit, offset", [
    ("en_US", 5, 0),
    ("es_MX", 10, 5),
    (None, 5, 0),
])
def test_get_categories_should_return_200(spotify_client, locale, limit, offset):
    response = spotify_client.get_categories(locale=locale, limit=limit, offset=offset)
    assert_status_code_ok(response, 200, "Get categories with optional params")
    json = response.json()
    assert "categories" in json
    assert_keys_exist(json["categories"], ["items", "limit", "offset", "total"])


# ===========================
# Optional Parameters
# ===========================

@pytest.mark.optional_fields
@pytest.mark.positive
@pytest.mark.parametrize("country", ["US", "IL", None])
def test_get_categories_with_country_param(spotify_client, country):
    response = spotify_client.get_categories(country=country)
    assert_status_code_ok(response, 200, f"Get categories with country={country}")
    assert "categories" in response.json()


@pytest.mark.optional_fields
@pytest.mark.positive
@pytest.mark.parametrize("limit", [1, 20, 50])
def test_get_categories_limit_boundary(spotify_client, limit):
    response = spotify_client.get_categories(limit=limit)
    assert_status_code_ok(response, 200, f"Get categories with limit={limit}")
    assert response.json()["categories"]["limit"] == limit


@pytest.mark.optional_fields
@pytest.mark.positive
def test_get_categories_with_offset(spotify_client):
    response = spotify_client.get_categories(limit=5, offset=5)
    assert_status_code_ok(response, 200, "Get categories with offset=5")


# ===========================
# Negative
# ===========================

@pytest.mark.negative
def test_get_categories_without_token_should_return_400_or_401():
    unauthenticated_client = SpotifyClient(request_handler=RequestHandler(token=""))
    response = unauthenticated_client.get_categories()
    assert_error_response(
        response,
        expected_status_codes=[400, 401],
        expected_message_substring="Only valid bearer"
    )


@pytest.mark.negative
def test_get_categories_with_invalid_limit_should_return_400(spotify_client):
    response = spotify_client.get_categories(limit=-10)
    assert_error_response(response, expected_status_codes=400, expected_message_substring="limit")


@pytest.mark.negative
def test_get_categories_with_invalid_offset_should_return_400(spotify_client):
    response = spotify_client.get_categories(offset=-5)
    assert_error_response(response, expected_status_codes=400, expected_message_substring="offset")


@pytest.mark.behavior
def test_get_categories_with_invalid_locale_should_fallback_to_default(spotify_client):
    """
    According to actual Spotify behavior, invalid locale strings are ignored and fallback applies.
    """
    response = spotify_client.get_categories(locale="invalid_LOCALE")
    assert_status_code_ok(response, 200, "Invalid locale should fallback to default")
    payload = response.json()
    assert "categories" in payload
    assert_keys_exist(payload["categories"], ["items", "limit", "offset", "total"])
