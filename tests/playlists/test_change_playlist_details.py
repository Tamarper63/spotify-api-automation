import pytest
from utils.assertion_manager import assert_status_code_ok


@pytest.mark.positive
@pytest.mark.parametrize("name, public, collaborative, description", [
    ("Automation Playlist", True, False, "Updated via automation test"),
    ("Hidden Playlist", False, None, "Private playlist"),
    ("Collab Playlist", None, True, None),
    ("Just Name", None, None, None),
    (None, None, None, "Only description changed"),
])
def test_change_playlist_details_optional_params_should_return_200(
    user_api_clients, default_playlist_id, name, public, collaborative, description
):
    response = user_api_clients.playlist.change_playlist_details(
        playlist_id=default_playlist_id,
        name=name,
        public=public,
        collaborative=collaborative,
        description=description
    )
    assert_status_code_ok(response, 200, "Change playlist details with optional params")


@pytest.mark.negative
def test_change_playlist_invalid_id_should_return_400(user_api_clients):
    response = user_api_clients.playlist.change_playlist_details(
        playlist_id="invalid_playlist_123",
        name="Invalid ID Test"
    )
    assert response.status_code == 400


@pytest.mark.negative
def test_change_playlist_without_auth(default_playlist_id):
    from infra.api_clients.playlist_client import PlaylistClient
    from infra.http.request_handler import RequestHandler

    client = PlaylistClient(RequestHandler(token=""))  # no token
    response = client.change_playlist_details(
        playlist_id=default_playlist_id,
        name="Unauth test"
    )
    assert response.status_code == 400


@pytest.mark.negative
def test_change_playlist_with_invalid_data(user_api_clients, default_playlist_id):
    # Intentionally send invalid type to trigger schema validation or 400
    response = user_api_clients.playlist.change_playlist_details(
        playlist_id=default_playlist_id,
        name=123456  # Invalid type
    )
    assert response.status_code == 500
