class PlaylistClient:
    def __init__(self, request_handler):
        self.base_url = "https://api.spotify.com/v1"
        self.req = request_handler

    def get_playlist(self, playlist_id: str, params: dict = None):
        url = f"{self.base_url}/playlists/{playlist_id}"
        return self.req.get(url, params=params or {})
