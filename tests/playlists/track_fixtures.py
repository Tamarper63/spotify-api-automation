# tests/playlists/track_fixtures.py
import pytest
from utils.yaml_loader import load_yaml_data


@pytest.fixture(scope="session")
def sample_uris() -> list[str]:
    data = load_yaml_data("track_uris.yaml")
    return data.get("valid_uris", [])


@pytest.fixture(scope="session")
def invalid_track_uri() -> str:
    data = load_yaml_data("track_uris.yaml")
    return data.get("invalid_uri", "spotify:track:invalid123")
