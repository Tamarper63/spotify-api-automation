from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class ExternalUrls(BaseModel):
    spotify: HttpUrl


class Owner(BaseModel):
    display_name: Optional[str]
    id: str
    type: str
    uri: str


class TrackItem(BaseModel):
    added_at: Optional[str]
    track: Optional[dict]  # Could be replaced with Track model for full validation


class Tracks(BaseModel):
    href: HttpUrl
    total: int
    items: Optional[List[TrackItem]]


class PlaylistResponse(BaseModel):
    id: str
    name: str
    public: Optional[bool]
    description: Optional[str]
    external_urls: ExternalUrls
    href: HttpUrl
    owner: Owner
    tracks: Tracks
    type: str
    uri: str


class Track(BaseModel):
    id: Optional[str]
    name: Optional[str]
    uri: Optional[str]
    duration_ms: Optional[int]
    explicit: Optional[bool]
    href: Optional[HttpUrl]
    preview_url: Optional[str]
    type: Optional[str]


class PlaylistTrackResponse(BaseModel):
    href: HttpUrl
    items: List[TrackItem]
    limit: Optional[int]
    next: Optional[str]
    offset: Optional[int]
    previous: Optional[str]
    total: int


class PlaylistItem(BaseModel):
    added_at: str
    track: dict
