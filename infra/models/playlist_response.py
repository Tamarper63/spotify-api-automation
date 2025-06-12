# utils/models/playlist.py

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ExternalUrl:
    spotify: str


@dataclass
class Image:
    url: str
    height: Optional[int]
    width: Optional[int]


@dataclass
class PlaylistOwner:
    id: str
    display_name: str
    href: str
    uri: str
    type: str
    external_urls: ExternalUrl


@dataclass
class PlaylistTrackInfo:
    href: str
    total: int
    limit: int
    offset: int
    previous: Optional[str]
    next: Optional[str]


@dataclass
class Followers:
    href: Optional[str]
    total: int


@dataclass
class PlaylistResponse:
    collaborative: bool
    description: Optional[str]
    external_urls: ExternalUrl
    href: str
    id: str
    images: List[Image]
    name: str
    owner: PlaylistOwner
    public: Optional[bool]
    snapshot_id: str
    tracks: PlaylistTrackInfo
    type: str
    uri: str
    followers: Optional[Followers] = None
    primary_color: Optional[str] = None
