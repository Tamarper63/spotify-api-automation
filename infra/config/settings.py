from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic.v1 import Extra


class Settings(BaseSettings):
    """
    Centralized configuration class for environment variables,
    loaded automatically from .env via pydantic.
    """

    spotify_client_id: str = Field(validation_alias="SPOTIFY_CLIENT_ID")
    spotify_client_secret: str = Field(validation_alias="SPOTIFY_CLIENT_SECRET")
    spotify_redirect_uri: str = Field(validation_alias="SPOTIFY_REDIRECT_URI")
    default_playlist_id: str = Field(
        default="7yyTti5oj0AYY68Zlocb1z", validation_alias="DEFAULT_PLAYLIST_ID"
    )
    spotify_refresh_token: str = Field(validation_alias="SPOTIFY_REFRESH_TOKEN")
    spotify_user_access_token: str = Field(
        default="", validation_alias="SPOTIFY_USER_ACCESS_TOKEN"
    )
    spotify_user_expires_at: str = Field(
        default="0", validation_alias="SPOTIFY_USER_EXPIRES_AT"
    )

    class Config:
        extra = Extra.ignore
        env_file = ".env"
        env_file_encoding = "utf-8"


_instance: Settings | None = None


def get_settings() -> Settings:
    """
    Return cached instance of Settings or create a new one if not yet initialized.
    """
    global _instance
    if _instance is None:
        _instance = Settings()
    return _instance
