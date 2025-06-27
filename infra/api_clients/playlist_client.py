class PlaylistClient:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_playlist(self, playlist_id: str, market: str = None, fields: str = None, additional_types: str = None):
        params = {}
        if market:
            params["market"] = market
        if fields:
            params["fields"] = fields
        if additional_types:
            params["additional_types"] = additional_types
        return self.request_handler.get(f"/playlists/{playlist_id}", params=params or None)

    def create_playlist(self, user_id: str, name: str, public=True, collaborative=False, description=""):
        payload = {
            "name": name,
            "public": public,
            "collaborative": collaborative,
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
        return self.request_handler.delete_with_body(f"/playlists/{playlist_id}/tracks", json=payload)

    def get_playlist_items(self, playlist_id: str, market: str = None, fields: str = None, limit: int = None,
                           offset: int = None):
        params = {}
        if market:
            params["market"] = market
        if fields:
            params["fields"] = fields
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self.request_handler.get(f"/playlists/{playlist_id}/tracks", params=params or None)

    def change_playlist_details(
            self,
            playlist_id: str,
            name: str = None,
            public: bool = None,
            collaborative: bool = None,
            description: str = None
    ):
        payload = {}
        if name is not None:
            payload["name"] = name
        if public is not None:
            payload["public"] = public
        if collaborative is not None:
            payload["collaborative"] = collaborative
        if description is not None:
            payload["description"] = description

        return self.request_handler.put(f"/playlists/{playlist_id}", json=payload)

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

    def reorder_or_replace_tracks(
            self,
            playlist_id: str,
            uris: list[str] = None,
            range_start: int = None,
            insert_before: int = None,
            range_length: int = None,
            snapshot_id: str = None
    ):
        payload = {}

        if uris is not None:
            payload["uris"] = uris
        if range_start is not None and insert_before is not None:
            payload["range_start"] = range_start
            payload["insert_before"] = insert_before
            if range_length is not None:
                payload["range_length"] = range_length
        if snapshot_id is not None:
            payload["snapshot_id"] = snapshot_id

        return self.request_handler.put(f"/playlists/{playlist_id}/tracks", json=payload)

    def upload_custom_playlist_cover_image(self, playlist_id: str, image_base64: str):
        headers = self.request_handler.headers.copy()
        headers["Content-Type"] = "image/jpeg"
        return self.request_handler.put(f"/playlists/{playlist_id}/images", json=None, data=image_base64,
                                        custom_headers=headers)

    def follow_playlist(self, playlist_id: str, public: bool = True):
        """
        Follow a playlist as the current user.
        'public' default True publishes to user profile; False makes it private.
        """
        return self.request_handler.put(
            f"/playlists/{playlist_id}/followers",
            json={"public": public},
        )

    def unfollow_playlist(self, playlist_id: str):
        """
        Unfollow a playlist as the current user.
        """
        return self.request_handler.delete(
            f"/playlists/{playlist_id}/followers"
        )
