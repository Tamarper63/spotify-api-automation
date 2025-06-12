from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PlaylistOwner:
    id: str
    display_name: str


@dataclass
class PlaylistTrackInfo:
    total: int


@dataclass
class PlaylistResponse:
    id: str
    name: str
    description: Optional[str]
    public: Optional[bool]
    owner: PlaylistOwner
    tracks: PlaylistTrackInfo
