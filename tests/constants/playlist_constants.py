# tests/constants/playlist_constants.py

# Request input values
DEFAULT_PLAYLIST_NAME = "API Created Playlist"
DEFAULT_DESCRIPTION = "Playlist created for automation test"
CONTRACT_PLAYLIST_NAME = "Contract Check Playlist"
MISSING_NAME_PLAYLIST = ""
NO_TOKEN_PLAYLIST_NAME = "No Token Playlist"
VALID_USER_ID = "spotify"

# Expected keys in create_playlist response
CREATE_PLAYLIST_KEYS = {
    "id", "name", "public", "description",
    "external_urls", "href", "owner", "tracks", "type", "uri"
}

# Parametrize cases
INVALID_USER_ID_CASES = [
    ("invalid_user_123", 403),
    ("", 400),
    (None, 403),
]
