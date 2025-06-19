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


# For parametrize
INVALID_PLAYLIST_IDS = ["invalid_id", "123", "!!!"]
INVALID_MARKET = "INVALID"
VALID_MARKET = "ES"
NESTED_FIELDS = "tracks.items(track(name,href))"
SIMPLE_FIELDS = "description,uri"
ADDITIONAL_TYPES = "episode"

# Playlist URL for unauth test
DEFAULT_PLAYLIST_URL = "https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n"

GET_PLAYLIST_ITEMS_KEYS = ["items", "href", "limit", "total"]

PLAYLIST_ITEMS_KEYS = ["items", "href", "limit", "total"]

DEFAULT_STATUS_OK = 200

EXPECTED_KEYS_GET_PLAYLIST_ITEMS = [
    "items",
    "href",
    "limit",
    "total"
]

PLAYLIST_ITEMS_OPTIONAL_PARAMS_FILE = "playlist_items_params.yaml"

UNAUTHORIZED = 401
BAD_REQUEST = 400

ERROR_MSGS = {
    "invalid_client": "invalid client",
    "missing_auth": "authorization",
    "missing_credentials": "Missing required credentials",
}