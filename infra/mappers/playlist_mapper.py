import requests
from infra.models.playlist_response import PlaylistResponse, PlaylistOwner, PlaylistTrackInfo


def map_playlist_response(response: requests.Response) -> PlaylistResponse:
    data = response.json()
    return PlaylistResponse(
        id=data["id"],
        name=data["name"],
        description=data.get("description"),
        public=data.get("public"),
        owner=PlaylistOwner(**data["owner"]),
        tracks=PlaylistTrackInfo(**data["tracks"])
    )
