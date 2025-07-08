# infra/models/playlist_response.py
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class ExternalUrls(BaseModel):
    spotify: str


class Image(BaseModel):
    url: str
    height: Optional[int]
    width: Optional[int]


class Owner(BaseModel):
    id: str
    display_name: Optional[str]
    uri: Optional[str]
    external_urls: Optional[ExternalUrls]
    type: Optional[str]


class Track(BaseModel):
    uri: str


class PlaylistItem(BaseModel):
    track: Track


class Tracks(BaseModel):
    href: str
    total: int
    items: Optional[List[PlaylistItem]]


class PlaylistResponse(BaseModel):
    collaborative: bool
    description: Optional[str]
    external_urls: ExternalUrls
    href: str
    id: str
    images: Optional[List[Image]] = Field(default_factory=list)
    name: str
    owner: Owner
    primary_color: Optional[str]
    public: Optional[bool]
    snapshot_id: str
    tracks: Tracks
    type: str
    uri: str


class PlaylistTrackResponse(BaseModel):
    href: str
    items: List[PlaylistItem]
    limit: int
    next: Optional[str]
    offset: int
    previous: Optional[str]
    total: int
