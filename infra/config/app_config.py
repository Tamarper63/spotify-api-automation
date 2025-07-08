from pydantic_settings import BaseSettings
from pydantic import Field


class AppConfig(BaseSettings):
    client_id: str = Field(..., alias="SPOTIFY_CLIENT_ID")
    client_secret: str = Field(..., alias="SPOTIFY_CLIENT_SECRET")
    token_url: str = Field(default="https://accounts.spotify.com/api/token", alias="SPOTIFY_TOKEN_URL")
    base_url: str = Field(default="https://api.spotify.com/v1", alias="SPOTIFY_BASE_URL")
    timeout: int = Field(default=10, alias="TIMEOUT")
    env_name: str = Field(default="local", alias="ENV_NAME")
    user_access_token_ext: str = Field(default="", alias="USER_ACCESS_TOKEN_EXT")
    spotify_redirect_uri: str = Field(..., alias="SPOTIFY_REDIRECT_URI")
    default_playlist_id: str = Field(..., alias="DEFAULT_PLAYLIST_ID")
    spotify_refresh_token: str = Field(..., alias="SPOTIFY_REFRESH_TOKEN")
    spotify_user_access_token: str = Field(default="", alias="SPOTIFY_USER_ACCESS_TOKEN")
    spotify_user_expires_at: str = Field(default="0", alias="SPOTIFY_USER_EXPIRES_AT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True
