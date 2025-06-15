class PlaylistClient:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_playlist(
        self,
        playlist_id: str,
        market: str = None,
        fields: str = None,
        additional_types: str = None
    ):
        params = {}
        if market:
            params["market"] = market
        if fields:
            params["fields"] = fields
        if additional_types:
            params["additional_types"] = additional_types

        return self.request_handler.get(f"/playlists/{playlist_id}", params=params or None)

    def create_playlist(self, user_id: str, name: str, public=True, description=""):
        payload = {
            "name": name,
            "public": public,
            "description": description
        }
        return self.request_handler.post(f"/users/{user_id}/playlists", json=payload)

    def add_tracks_to_playlist(self, playlist_id: str, uris: list[str], position: int = None):
        payload = {"uris": uris}
        if position is not None:
            payload["position"] = position

        return self.request_handler.post(f"/playlists/{playlist_id}/tracks", json=payload)

    def remove_tracks_from_playlist(self, playlist_id: str, uris: list[str]):
        payload = {
            "tracks": [{"uri": uri} for uri in uris]
        }
        return self.request_handler.delete(f"/playlists/{playlist_id}/tracks", json=payload)
