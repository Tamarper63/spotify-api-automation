import pytest
import requests

from infra.models.user_profile_response import UserProfileResponse
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_keys_exist,
)

# ======================
# Contract & Schema
# ======================


@pytest.mark.contract
def test_user_profile_model_schema(spotify_user_client):
    response = spotify_user_client.get_current_user_profile()
    assert_status_code_ok(response, 200)
    UserProfileResponse(**response.json())


# ======================
# Positive Tests
# ======================


@pytest.mark.smoke
@pytest.mark.positive
def test_get_current_user_profile_should_return_200(spotify_user_client):
    response = spotify_user_client.get_current_user_profile()
    assert_status_code_ok(response, 200, "Get current user profile")
    expected_keys = ["id", "display_name", "uri", "external_urls", "type"]
    assert_keys_exist(response.json(), expected_keys)


# ======================
# Negative Tests
# ======================


@pytest.mark.negative
def test_get_current_user_profile_without_token():
    response = requests.get("https://api.spotify.com/v1/me")
    assert response.status_code == 401
    assert "error" in response.json()


@pytest.mark.negative
def test_get_user_profile_with_invalid_token_should_return_401():
    headers = {"Authorization": "Bearer INVALID_TOKEN_123"}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    assert response.status_code == 401
    assert "error" in response.json()
    assert "Invalid access token" in response.json()["error"]["message"]


@pytest.mark.negative
def test_user_profile_should_not_include_email_if_scope_missing(spotify_user_client):
    response = spotify_user_client.get_current_user_profile()
    data = response.json()
    assert "email" not in data


# ======================
# Optional Fields
# ======================

OPTIONAL_FIELDS = [
    ("email", lambda v: "@" in v),
    ("display_name", lambda v: isinstance(v, str)),
    ("country", lambda v: isinstance(v, str) and len(v) == 2),
    ("product", lambda v: v in ["premium", "free", "open"]),
]


@pytest.mark.optional_fields
@pytest.mark.positive
@pytest.mark.parametrize("field, validator", OPTIONAL_FIELDS)
def test_user_profile_optional_field_behavior(spotify_user_client, field, validator):
    response = spotify_user_client.get_current_user_profile()
    assert_status_code_ok(response, 200, f"Optional field: {field}")

    json_data = response.json()
    if field in json_data:
        assert validator(
            json_data[field]
        ), f"❌ Field `{field}` present but value invalid: {json_data[field]}"
    else:
        pytest.skip(f"Optional field `{field}` not present in response")
