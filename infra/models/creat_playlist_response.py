from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict


class ExternalUrls(BaseModel):
    spotify: HttpUrl


class Owner(BaseModel):
    id: str
    type: str
    uri: str
    display_name: Optional[str]


class TracksInfo(BaseModel):
    href: HttpUrl
    total: int


class CreatePlaylistResponse(BaseModel):
    id: str
    name: str
    public: Optional[bool]
    description: Optional[str]
    external_urls: ExternalUrls
    href: HttpUrl
    owner: Owner
    tracks: TracksInfo
    type: str
    uri: str
