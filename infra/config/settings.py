# settings.py
from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic.v1 import Extra


class Settings(BaseSettings):
    spotify_client_id: str = Field(validation_alias="SPOTIFY_CLIENT_ID")
    spotify_client_secret: str = Field(validation_alias="SPOTIFY_CLIENT_SECRET")

    class Config:
        extra = Extra.ignore
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()