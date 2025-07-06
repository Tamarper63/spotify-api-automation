import pytest
from utils.assertion_manager import (
    assert_status_code_ok,
    assert_keys_exist,
    assert_error_response,
)


@pytest.mark.contract
@pytest.mark.integration
@pytest.mark.parametrize(
    "q, types",
    [
        ("Nirvana", ["artist"]),
        ("Come As You Are", ["track"]),
        ("Nevermind", ["album"]),
        ("Nirvana", ["artist", "track"]),
    ],
)
def test_search_various_types_ok(spotify_user_client, q, types):
    response = spotify_user_client.search(
        query=q, types=types, market="US", limit=5, offset=0
    )
    assert_status_code_ok(response, 200)
    payload = response.json()

    for t in types:
        key = f"{t}s"
        assert key in payload, f"Expected key '{key}' in response"
        assert_keys_exist(payload[key], ["items", "limit", "offset", "total"])


@pytest.mark.positive
def test_search_with_include_external_audio(spotify_user_client):
    response = spotify_user_client.search(
        query="Nirvana", types=["track"], market="US", limit=5, include_external="audio"
    )
    assert_status_code_ok(response, 200, "Search with include_external=audio")
    json_data = response.json()
    assert "tracks" in json_data
    assert "items" in json_data["tracks"]


@pytest.mark.positive
def test_search_with_offset(spotify_user_client):
    response = spotify_user_client.search(
        query="Nirvana", types=["track"], market="US", offset=5
    )
    assert_status_code_ok(response, 200, "Search with offset")
    json_data = response.json()
    assert "tracks" in json_data
    assert "offset" in json_data["tracks"]
    assert json_data["tracks"]["offset"] == 5


@pytest.mark.positive
def test_search_with_all_optional_params(spotify_user_client):
    response = spotify_user_client.search(
        query="Nirvana",
        types=["track"],
        market="US",
        limit=3,
        offset=2,
        include_external="audio",
    )
    assert_status_code_ok(response, 200, "Search with all optional params")
    json_data = response.json()
    assert "tracks" in json_data
    assert json_data["tracks"]["limit"] == 3
    assert json_data["tracks"]["offset"] == 2


@pytest.mark.negative
def test_search_missing_q(spotify_user_client):
    response = spotify_user_client.search(query="", types=["track"])
    assert_error_response(response, expected_status_codes=400)


@pytest.mark.negative
def test_search_unauthorized():
    import requests

    response = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": "Nirvana", "type": "track", "market": "US"},
    )
    assert response.status_code in (401, 403)


@pytest.mark.negative
def test_search_with_invalid_type_should_return_400(spotify_user_client):
    response = spotify_user_client.search(query="Nirvana", types=["invalidtype"])
    assert_error_response(
        response, expected_status_codes=400, expected_message_substring="type"
    )
