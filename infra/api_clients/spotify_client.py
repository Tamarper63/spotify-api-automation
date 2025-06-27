# spotify_client.py – Unified Client
import base64
from pydantic_core import ValidationError
from infra.http.request_sender import _send_request
from infra.config.settings import get_settings


class SpotifyClient:
    def __init__(self, request_handler=None, client_id: str = None, client_secret: str = None):
        self.request_handler = request_handler
        settings = get_settings()

        self.client_id = client_id or settings.spotify_client_id
        self.client_secret = client_secret or settings.spotify_client_secret
        self.token_url = "https://accounts.spotify.com/api/token"

    # ===========================
    # Token Handling
    # ===========================

    def get_token_response(self, raw: bool = False):
        headers = {
            "Authorization": f"Basic {self._encode_credentials()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        response = _send_request(url=self.token_url, method="POST", headers=headers, data=data)
        return response if raw else response.json()

    def _encode_credentials(self) -> str:
        return base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

    # ===========================
    # User
    # ===========================

    def get_current_user_profile(self):
        return self.request_handler.get("/me")

    # ===========================
    # Playlist
    # ===========================

    def create_playlist(self, user_id: str, name: str, public=True, collaborative=False, description=""):
        return self.request_handler.post(f"/users/{user_id}/playlists", json={
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description
        })

    def add_tracks_to_playlist(self, playlist_id: str, uris: list[str], position: int = None):
        payload = {"uris": uris}
        if position is not None:
            payload["position"] = position
        return self.request_handler.post(f"/playlists/{playlist_id}/tracks", json=payload)

    def get_playlist(self, playlist_id: str, market=None, fields=None, additional_types=None):
        params = {k: v for k, v in {
            "market": market, "fields": fields, "additional_types": additional_types
        }.items() if v is not None}
        return self.request_handler.get(f"/playlists/{playlist_id}", params=params or None)

    def get_playlist_items(self, playlist_id: str, market=None, fields=None, limit=None, offset=None):
        params = {k: v for k, v in {
            "market": market, "fields": fields, "limit": limit, "offset": offset
        }.items() if v is not None}
        return self.request_handler.get(f"/playlists/{playlist_id}/tracks", params=params or None)

    def change_playlist_details(self, playlist_id: str, name=None, public=None, collaborative=None, description=None):
        payload = {k: v for k, v in {
            "name": name, "public": public, "collaborative": collaborative, "description": description
        }.items() if v is not None}
        return self.request_handler.put(f"/playlists/{playlist_id}", json=payload)

    def follow_playlist(self, playlist_id: str, public: bool = True):
        return self.request_handler.put(f"/playlists/{playlist_id}/followers", json={"public": public})

    def unfollow_playlist(self, playlist_id: str):
        return self.request_handler.delete(f"/playlists/{playlist_id}/followers")

    def remove_tracks_from_playlist(self, playlist_id: str, uris: list[str]):
        payload = {
            "tracks": [{"uri": uri} for uri in uris]
        }
        return self.request_handler.delete_with_body(f"/playlists/{playlist_id}/tracks", json=payload)

    def reorder_playlist_items(self, playlist_id: str, range_start: int, insert_before: int, range_length: int = 1,
                               snapshot_id: str = None):
        payload = {
            "range_start": range_start,
            "insert_before": insert_before,
            "range_length": range_length
        }
        if snapshot_id:
            payload["snapshot_id"] = snapshot_id
        return self.request_handler.put(f"/playlists/{playlist_id}/tracks", json=payload)

    def upload_custom_playlist_cover_image(self, playlist_id: str, image_base64: str):
        headers = self.request_handler.headers.copy()
        headers["Content-Type"] = "image/jpeg"
        return self.request_handler.put(
            f"/playlists/{playlist_id}/images",
            json=None,
            data=image_base64,
            custom_headers=headers
        )

    # ===========================
    # Browse
    # ===========================

    def get_featured_playlists(self, country=None, locale=None, timestamp=None, limit=None, offset=None):
        params = {k: v for k, v in {
            "country": country,
            "locale": locale,
            "timestamp": timestamp,
            "limit": limit,
            "offset": offset
        }.items() if v is not None}
        return self.request_handler.get("/browse/featured-playlists", params=params)

    # ===========================
    # Search
    # ===========================

    def search(self, query: str, types: list[str], market=None, limit=None, offset=None, include_external=None):
        params = {
            "q": query,
            "type": ",".join(types)
        }
        if market:
            params["market"] = market
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if include_external:
            params["include_external"] = include_external
        return self.request_handler.get("/search", params=params)

    def get_categories(self, country=None, locale=None, limit=None, offset=None):
        params = {k: v for k, v in {
            "country": country,
            "locale": locale,
            "limit": limit,
            "offset": offset
        }.items() if v is not None}
        return self.request_handler.get("/browse/categories", params=params)

