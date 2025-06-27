import requests
from pydantic import ValidationError, BaseModel

from infra.models.error_response import ErrorResponse
from infra.models.playlist_response import PlaylistTrackResponse, PlaylistItem
from tests.constants.playlist_constants import EXPECTED_KEYS_GET_PLAYLIST_ITEMS


def assert_status_code_ok(response, expected, context=""):
    if isinstance(expected, list):
        assert response.status_code in expected, (
            f"❌ {context}: Expected one of {expected}, got {response.status_code}. "
            f"Response: {response.text}"
        )
    else:
        assert response.status_code == expected, (
            f"❌ {context}: Expected {expected}, got {response.status_code}. "
            f"Response: {response.text}"
        )


def assert_keys_exist(response_json, keys):
    missing = [key for key in keys if key not in response_json]
    assert not missing, f"❌ Missing keys in response: {missing}"


def assert_json_field_equals(response, field: str, expected_value, context=""):
    response_json = response.json()
    actual = response_json.get(field)
    assert actual == expected_value, (
        f"❌ {context}: Expected `{field}` to be '{expected_value}', but got '{actual}'"
    )


def assert_json_matches_expected(response_json: dict, expected: dict, context=""):
    """
    Recursively assert that expected fields match in a JSON response.
    Supports nested keys using dot notation.
    """
    for key, expected_value in expected.items():
        if isinstance(expected_value, dict):
            # Recurse into nested dicts
            actual_sub_json = response_json.get(key, {})
            assert isinstance(actual_sub_json, dict), f"❌ {context}: `{key}` is not a dict in response"
            assert_json_matches_expected(actual_sub_json, expected_value, context=f"{context}.{key}")
        else:
            actual_value = response_json.get(key)
            assert actual_value == expected_value, (
                f"❌ {context}.{key}: Expected '{expected_value}', got '{actual_value}'"
            )


def assert_nested_field_equals(response_json: dict, field_path: str, expected_value, context=""):
    """
    Assert that a nested field (like 'owner.display_name') matches the expected value.
    """
    keys = field_path.split(".")
    current = response_json

    for key in keys:
        assert key in current, f"❌ Missing field `{field_path}` at `{key}`"
        current = current[key]

    assert current == expected_value, (
            f"❌ Mismatch at `{field_path}`: expected `{expected_value}`, got `{current}`"
            + (f" | Context: {context}" if context else "")
    )


def assert_token_is_valid(token: str):
    assert isinstance(token, str), "❌ Token must be a string"
    assert len(token) > 10, f"❌ Token is too short: {len(token)} chars"


def assert_error_response(
        response,
        expected_status_codes: int | list[int],
        expected_message_substring: str | None = None,
        context: str = "Error response validation"
):
    assert_status_code_ok(response, expected_status_codes, context)

    try:
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            # Handle raw HTML/invalid JSON response
            error_msg = response.text.strip()
            if expected_message_substring:
                assert expected_message_substring.lower() in error_msg.lower(), (
                    f"[{context}] HTML response — expected to find '{expected_message_substring}', "
                    f"but got:\n{error_msg}"
                )
            return  # success fallback

        # Handle Spotify-style JSON error
        if isinstance(data.get("error"), dict):
            from infra.models.error_response import ErrorResponse
            error_model = ErrorResponse(**data)
            error_msg = error_model.error.message
        else:
            error_msg = data.get("error_description") or str(data.get("error"))

        if expected_message_substring:
            assert expected_message_substring.lower() in error_msg.lower(), (
                f"[{context}] Expected error message to contain: '{expected_message_substring}', "
                f"but got: '{error_msg}'"
            )

    except Exception as e:
        raise AssertionError(f"[{context}] Failed to extract error message: {e}\nResponse: {response.text}")


def assert_playlist_items_response_keys_exist(response):
    response_json = response.json()
    assert_keys_exist(response_json, EXPECTED_KEYS_GET_PLAYLIST_ITEMS)
    assert isinstance(response_json["items"], list), "'items' must be a list"


def assert_playlist_items_match_model(response):
    items = response.json().get("items", [])
    for idx, item in enumerate(items):
        try:
            PlaylistTrackResponse(**item)
        except Exception as e:
            raise AssertionError(f"❌ Invalid item at index {idx}: {e}")


def assert_playlist_items_with_limit(response, expected_limit: int):
    actual_limit = response.json().get("limit")
    assert actual_limit == expected_limit, (
        f"❌ Limit mismatch: expected {expected_limit}, got {actual_limit}"
    )


def assert_playlist_items_schema(response):
    """
    Validates the full response and each item inside `items[]`.
    """
    json_data = response.json()

    # Validate full response structure
    PlaylistTrackResponse(**json_data)

    # Validate each item (optional but good)
    for idx, item in enumerate(json_data.get("items", [])):
        try:
            PlaylistItem(**item)
        except Exception as e:
            raise AssertionError(f"❌ Invalid playlist item at index {idx}: {e}")


def assert_response_schema(response: dict, schema_model: type[BaseModel], context: str = ""):
    """
    Validate that a response matches the expected schema.
    Raises an assertion error if validation fails.
    """
    try:
        schema_model.parse_obj(response)
    except ValidationError as e:
        raise AssertionError(
            f"❌ Schema validation failed{f' in {context}' if context else ''}:\n{e}"
        )


def ensure_tracks_exist_in_playlist(api_client, playlist_id: str, uris: list[str]):
    """
    Ensure the specified URIs exist in the playlist.
    If not present — add them.
    This is used for test setup only.
    """
    response = api_client.get_playlist_items(playlist_id, limit=100)
    assert_status_code_ok(response, 200, "Fetch playlist items for validation")

    existing_uris = {
        item["track"]["uri"]
        for item in response.json().get("items", [])
        if item.get("track") and item["track"].get("uri")
    }

    missing_uris = [uri for uri in uris if uri not in existing_uris]
    if missing_uris:
        add_resp = api_client.add_tracks_to_playlist(playlist_id, missing_uris)
        assert_status_code_ok(add_resp, 201, "Add tracks to playlist (test setup)")
