# infra/api_clients/spotify_client.py

import base64
import time
from infra.config.settings import get_settings
from infra.http.request_sender import _send_request
from utils.log_utils import log_api_call


class SpotifyClient:
    def __init__(self, request_handler=None, client_id: str = None, client_secret: str = None):
        self.request_handler = request_handler
        settings = get_settings()
        self.client_id = client_id or settings.spotify_client_id
        self.client_secret = client_secret or settings.spotify_client_secret
        self.token_url = "https://accounts.spotify.com/api/token"

    def _log_and_call(self, method: str, url: str, *, http_method: str, **kwargs):
        start = time.perf_counter()
        response = getattr(self.request_handler, http_method)(url, **kwargs)
        elapsed = int((time.perf_counter() - start) * 1000)
        try:
            log_api_call(
                method=method,
                url=url,
                status_code=response.status_code,
                elapsed_ms=elapsed,
                response_body=response.json() if hasattr(response, "json") else None
            )
        except Exception:
            pass
        return response

    def _encode_credentials(self) -> str:
        return base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

    def get_token_response(self, raw: bool = False):
        headers = {
            "Authorization": f"Basic {self._encode_credentials()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        response = _send_request(url=self.token_url, method="POST", headers=headers, data=data)
        return response if raw else response.json()

    def get_current_user_profile(self):
        return self._log_and_call("get_current_user_profile", "/me", http_method="get")

    def create_playlist(self, user_id: str, name: str, public=True, collaborative=False, description=""):
        payload = {
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description
        }
        return self._log_and_call("create_playlist", f"/users/{user_id}/playlists", http_method="post", json=payload)

    def add_tracks_to_playlist(self, playlist_id: str, uris: list[str], position: int = None):
        payload = {"uris": uris}
        if position is not None:
            payload["position"] = position
        return self._log_and_call("add_tracks_to_playlist", f"/playlists/{playlist_id}/tracks", http_method="post", json=payload)

    def get_playlist(self, playlist_id: str, market=None, fields=None, additional_types=None):
        params = {
            "market": market,
            "fields": fields,
            "additional_types": additional_types
        }
        return self._log_and_call("get_playlist", f"/playlists/{playlist_id}", http_method="get", params={k: v for k, v in params.items() if v is not None})

    def get_playlist_items(self, playlist_id: str, market=None, fields=None, limit=None, offset=None):
        params = {
            "market": market,
            "fields": fields,
            "limit": limit,
            "offset": offset
        }
        return self._log_and_call("get_playlist_items", f"/playlists/{playlist_id}/tracks", http_method="get", params={k: v for k, v in params.items() if v is not None})

    def change_playlist_details(self, playlist_id: str, name=None, public=None, collaborative=None, description=None):
        payload = {
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description
        }
        return self._log_and_call("change_playlist_details", f"/playlists/{playlist_id}", http_method="put", json={k: v for k, v in payload.items() if v is not None})

    def follow_playlist(self, playlist_id: str, public: bool = True):
        return self._log_and_call("follow_playlist", f"/playlists/{playlist_id}/followers", http_method="put", json={"public": public})

    def unfollow_playlist(self, playlist_id: str):
        return self._log_and_call("unfollow_playlist", f"/playlists/{playlist_id}/followers", http_method="delete")

    def remove_tracks_from_playlist(self, playlist_id: str, uris: list[str]):
        payload = {"tracks": [{"uri": uri} for uri in uris]}
        return self._log_and_call("remove_tracks_from_playlist", f"/playlists/{playlist_id}/tracks", http_method="delete", json=payload)

    def reorder_playlist_items(self, playlist_id: str, range_start: int, insert_before: int, range_length: int = 1, snapshot_id: str = None):
        payload = {
            "range_start": range_start,
            "insert_before": insert_before,
            "range_length": range_length
        }
        if snapshot_id:
            payload["snapshot_id"] = snapshot_id
        return self._log_and_call("reorder_playlist_items", f"/playlists/{playlist_id}/tracks", http_method="put", json=payload)

    def upload_custom_playlist_cover_image(self, playlist_id: str, image_base64: str):
        headers = self.request_handler.headers.copy()
        headers["Content-Type"] = "image/jpeg"
        return self._log_and_call("upload_playlist_cover", f"/playlists/{playlist_id}/images", http_method="put", json=None, data=image_base64, custom_headers=headers)

    def get_featured_playlists(self, country=None, locale=None, timestamp=None, limit=None, offset=None):
        params = {
            "country": country,
            "locale": locale,
            "timestamp": timestamp,
            "limit": limit,
            "offset": offset
        }
        return self._log_and_call("get_featured_playlists", "/browse/featured-playlists", http_method="get", params={k: v for k, v in params.items() if v is not None})

    def get_categories(self, country=None, locale=None, limit=None, offset=None):
        params = {
            "country": country,
            "locale": locale,
            "limit": limit,
            "offset": offset
        }
        return self._log_and_call("get_categories", "/browse/categories", http_method="get", params={k: v for k, v in params.items() if v is not None})

    def search(self, query: str, types: list[str], market=None, limit=None, offset=None, include_external=None):
        params = {
            "q": query,
            "type": ",".join(types),
            "market": market,
            "limit": limit,
            "offset": offset,
            "include_external": include_external
        }
        return self._log_and_call("search", "/search", http_method="get", params={k: v for k, v in params.items() if v is not None})
