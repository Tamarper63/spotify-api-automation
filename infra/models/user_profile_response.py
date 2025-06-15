from pydantic import BaseModel, Field
from typing import Optional, Dict


class ExternalUrls(BaseModel):
    spotify: str


class UserProfileResponse(BaseModel):
    display_name: Optional[str] = None
    external_urls: ExternalUrls
    href: str
    id: str
    type: str
    uri: str
    email: Optional[str] = None
    country: Optional[str] = None
    product: Optional[str] = None
