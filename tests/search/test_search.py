import pytest
from utils.assertion_manager import assert_status_code_ok, assert_keys_exist


@pytest.mark.contract
@pytest.mark.integration
@pytest.mark.parametrize("q, types", [
    ("Nirvana", ["artist"]),
    ("Come As You Are", ["track"]),
    ("Nevermind", ["album"]),
    ("Nirvana", ["artist", "track"]),
])
def test_search_various_types_ok(user_api_clients, q, types):
    response = user_api_clients.spotify.search(
        query=q,
        types=types,
        market="US",
        limit=5,
        offset=0
    )
    assert_status_code_ok(response, 200)
    payload = response.json()

    for t in types:
        key = f"{t}s"  # plural
        assert key in payload, f"Expected key '{key}' in response"
        assert_keys_exist(payload[key], ["items", "limit", "offset", "total"])


@pytest.mark.negative
def test_search_missing_q(user_api_clients):
    response = user_api_clients.spotify.search(query="", types=["track"])
    assert response.status_code == 400


@pytest.mark.negative
def test_search_unauthorized():
    import requests
    response = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": "Nirvana", "type": "track", "market": "US"}
    )
    assert response.status_code in (401, 403)
