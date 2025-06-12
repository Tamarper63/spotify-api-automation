def assert_status_code_ok(response, expected, context=""):
    assert response.status_code == expected, (
        f"❌ {context}: Expected {expected}, got {response.status_code}. "
        f"Response: {response.text}"
    )


def assert_keys_exist(response_json, keys):
    missing = [key for key in keys if key not in response_json]
    assert not missing, f"❌ Missing keys in response: {missing}"
