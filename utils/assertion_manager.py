def assert_status_code_ok(response, expected, context=""):
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


#
# def assert_error_response(response, expected_status: int, expected_message_substring: str = ""):
#     assert response.status_code == expected_status, (
#         f"❌ Expected status {expected_status}, got {response.status_code}. Response: {response.text}"
#     )
#
#     body = response.json()
#     assert "error" in body, "❌ 'error' object missing in response"
#
#     error = body["error"]
#     assert "status" in error and "message" in error, "❌ 'status' or 'message' key missing in 'error' object"
#
#     assert error["status"] == expected_status, (
#         f"❌ Error status mismatch. Expected: {expected_status}, Got: {error['status']}"
#     )
#
#     if expected_message_substring:
#         assert expected_message_substring.lower() in error["message"].lower(), (
#             f"❌ Error message does not contain expected text. "
#             f"Expected to include: '{expected_message_substring}', Got: '{error['message']}'"
#         )


def assert_token_is_valid(token: str):
    assert isinstance(token, str), "❌ Token must be a string"
    assert len(token) > 10, f"❌ Token is too short: {len(token)} chars"


def assert_error_response(
        response,
        expected_status: int = None,
        expected_status_codes: list[int] = None,
        expected_message_substring: str = ""
):
    """
    Assert that an error response matches expected status and optional message.
    Either `expected_status` or `expected_status_codes` must be provided.
    """

    # Determine which status codes to expect
    if expected_status is not None:
        expected_status_codes = [expected_status]
    elif expected_status_codes is None:
        expected_status_codes = [400, 401, 403, 404, 422]  # default safe fallback

    assert response.status_code in expected_status_codes, (
        f"❌ Expected status in {expected_status_codes}, got {response.status_code}. Response: {response.text}"
    )

    try:
        body = response.json()
    except ValueError:
        raise AssertionError("❌ Response is not valid JSON")

    assert "error" in body, "❌ 'error' object missing in response"

    error = body["error"]
    assert "status" in error and "message" in error, "❌ 'status' or 'message' key missing in 'error' object"

    if expected_status is not None:
        assert error["status"] == expected_status, (
            f"❌ Error status mismatch. Expected: {expected_status}, Got: {error['status']}"
        )

    if expected_message_substring:
        assert expected_message_substring.lower() in error["message"].lower(), (
            f"❌ Error message mismatch.\nExpected to include: '{expected_message_substring}'\n"
            f"Actual message: '{error['message']}'"
        )
