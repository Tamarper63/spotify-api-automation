from typing import List
from infra.request_handler import RequestHandler
import requests


class PlaylistClient:
    """
    Spotify Playlist Client — handles playlist-related API operations
    using a provided RequestHandler instance.
    """

    def __init__(self, request_handler: RequestHandler):
        self.req = request_handler
        self.base_url = "https://api.spotify.com/v1"

    def create_playlist(self, user_id: str, name: str, public: bool = True) -> requests.Response:
        """
        Create a playlist for a given user.

        :param user_id: Spotify user ID
        :param name: Name of the new playlist
        :param public: Whether the playlist is public
        :return: Raw requests.Response object
        """
        url = f"{self.base_url}/users/{user_id}/playlists"
        payload = {"name": name, "public": public}

        response = self.req.post(url=url, json=payload)
        return response  # Raw response (caller handles status/assertions)

    def add_tracks(self, playlist_id: str, uris: List[str]) -> requests.Response:
        """
        Add a list of track URIs to an existing playlist.

        :param playlist_id: ID of the playlist to modify
        :param uris: List of Spotify track URIs
        :return: Raw requests.Response object
        """
        url = f"{self.base_url}/playlists/{playlist_id}/tracks"
        payload = {"uris": uris}

        response = self.req.post(url=url, json=payload)
        return response

    def get_playlist(self, playlist_id: str) -> requests.Response:
        """
        Retrieve details of a specific playlist.

        :param playlist_id: ID of the playlist
        :return: Raw requests.Response object
        """
        url = f"{self.base_url}/playlists/{playlist_id}"

        response = self.req.get(url=url)
        return response
