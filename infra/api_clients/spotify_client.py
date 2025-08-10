# infra/api_clients/spotify_client.py

from __future__ import annotations
from typing import Any, Dict, Optional, List
from infra.config.loader import load_config
from infra.auth.token_provider import get_token_response as get_app_token


class SpotifyClient:
    """
    Thin API client. No logging / HTTP here.
    Delegates all HTTP to RequestHandler (base_url join, Authorization, retries/backoff, logging, 401 refresh).
    """

    def __init__(self, request_handler: Optional[Any] = None,
                 client_id: Optional[str] = None, client_secret: Optional[str] = None):
        # allow None for token-only tests
        self.request_handler = request_handler

        cfg = load_config()
        self.client_id = client_id or cfg.client_id
        self.client_secret = client_secret or cfg.client_secret
        self.token_url = "https://accounts.spotify.com/api/token"

    # --- Auth (kept for compatibility) ---
    def get_token_response(self, raw: bool = False) -> Dict[str, Any]:
        return get_app_token(self.client_id, self.client_secret, raw=raw)

    # --- Internal unified caller ---
    def _call(self, name: str, endpoint: str, *, method: str, **kwargs) -> Any:
        if self.request_handler is None:
            raise RuntimeError("RequestHandler is required for endpoint calls")
        # RequestHandler.send returns requests.Response by project convention
        return self.request_handler.send(method=method, endpoint=endpoint, **kwargs)

    # --- Endpoints ---

    def get_current_user_profile(self):
        return self._call("get_current_user_profile", "/me", method="GET")

    def create_playlist(self, user_id: str, name: str,
                        public: bool = True, collaborative: bool = False, description: str = ""):
        payload = {
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description,
        }
        return self._call("create_playlist", f"/users/{user_id}/playlists", method="POST", json=payload)

    def add_tracks_to_playlist(self, playlist_id: str, uris: List[str], position: Optional[int] = None):
        payload: Dict[str, Any] = {"uris": uris}
        if position is not None:
            payload["position"] = position
        return self._call("add_tracks_to_playlist", f"/playlists/{playlist_id}/tracks", method="POST", json=payload)

    def get_playlist(self, playlist_id: str,
                     market: Optional[str] = None, fields: Optional[str] = None, additional_types: Optional[str] = None):
        params = {k: v for k, v in {
            "market": market, "fields": fields, "additional_types": additional_types
        }.items() if v is not None}
        return self._call("get_playlist", f"/playlists/{playlist_id}", method="GET", params=params)

    def get_playlist_items(self, playlist_id: str,
                           market: Optional[str] = None, fields: Optional[str] = None,
                           limit: Optional[int] = None, offset: Optional[int] = None):
        params = {k: v for k, v in {
            "market": market, "fields": fields, "limit": limit, "offset": offset
        }.items() if v is not None}
        return self._call("get_playlist_items", f"/playlists/{playlist_id}/tracks", method="GET", params=params)

    def change_playlist_details(self, playlist_id: str,
                                name: Optional[str] = None, public: Optional[bool] = None,
                                collaborative: Optional[bool] = None, description: Optional[str] = None):
        payload = {k: v for k, v in {
            "name": name, "public": public, "collaborative": collaborative, "description": description
        }.items() if v is not None}
        return self._call("change_playlist_details", f"/playlists/{playlist_id}", method="PUT", json=payload)

    def follow_playlist(self, playlist_id: str, public: bool = True):
        return self._call("follow_playlist", f"/playlists/{playlist_id}/followers", method="PUT", json={"public": public})

    def unfollow_playlist(self, playlist_id: str):
        return self._call("unfollow_playlist", f"/playlists/{playlist_id}/followers", method="DELETE")

    def remove_tracks_from_playlist(self, playlist_id: str, uris: List[str]):
        payload = {"tracks": [{"uri": uri} for uri in uris]}
        return self._call("remove_tracks_from_playlist", f"/playlists/{playlist_id}/tracks", method="DELETE", json=payload)

    def reorder_playlist_items(self, playlist_id: str, range_start: int, insert_before: int,
                               range_length: int = 1, snapshot_id: Optional[str] = None):
        payload: Dict[str, Any] = {"range_start": range_start, "insert_before": insert_before, "range_length": range_length}
        if snapshot_id:
            payload["snapshot_id"] = snapshot_id
        return self._call("reorder_playlist_items", f"/playlists/{playlist_id}/tracks", method="PUT", json=payload)

    def upload_custom_playlist_cover_image(self, playlist_id: str, image_base64: str):
        # pass content-type explicitly; handler adds Authorization
        headers = {"Content-Type": "image/jpeg"}
        return self._call("upload_playlist_cover", f"/playlists/{playlist_id}/images",
                          method="PUT", data=image_base64, headers=headers)

    def get_featured_playlists(self, country: Optional[str] = None, locale: Optional[str] = None,
                               timestamp: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None):
        params = {k: v for k, v in {
            "country": country, "locale": locale, "timestamp": timestamp, "limit": limit, "offset": offset
        }.items() if v is not None}
        return self._call("get_featured_playlists", "/browse/featured-playlists", method="GET", params=params)

    def get_categories(self, country: Optional[str] = None, locale: Optional[str] = None,
                       limit: Optional[int] = None, offset: Optional[int] = None):
        params = {k: v for k, v in {
            "country": country, "locale": locale, "limit": limit, "offset": offset
        }.items() if v is not None}
        return self._call("get_categories", "/browse/categories", method="GET", params=params)

    def search(self, query: str, types: List[str], market: Optional[str] = None,
               limit: Optional[int] = None, offset: Optional[int] = None, include_external: Optional[str] = None):
        params = {k: v for k, v in {
            "q": query,
            "type": ",".join(types),
            "market": market,
            "limit": limit,
            "offset": offset,
            "include_external": include_external,
        }.items() if v is not None}
        return self._call("search", "/search", method="GET", params=params)
