# infra/config/app_config.py
from pathlib import Path
from pydantic import Field, AliasChoices, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]  # עדכני עומק לפי הפרויקט

class AppConfig(BaseSettings):
    client_id: str = Field(..., validation_alias=AliasChoices("SPOTIFY_CLIENT_ID"))
    client_secret: SecretStr = Field(..., validation_alias=AliasChoices("SPOTIFY_CLIENT_SECRET"))
    spotify_redirect_uri: str = Field(..., validation_alias=AliasChoices("SPOTIFY_REDIRECT_URI"))
    default_playlist_id: str = Field(..., validation_alias=AliasChoices("DEFAULT_PLAYLIST_ID"))
    spotify_refresh_token: SecretStr = Field(..., validation_alias=AliasChoices("SPOTIFY_REFRESH_TOKEN"))

    token_url: str = Field("https://accounts.spotify.com/api/token", validation_alias=AliasChoices("SPOTIFY_TOKEN_URL"))
    base_url: str  = Field("https://api.spotify.com/v1",            validation_alias=AliasChoices("SPOTIFY_BASE_URL"))
    timeout: float = Field(10.0,  validation_alias=AliasChoices("TIMEOUT"))
    retries: int   = Field(3,     validation_alias=AliasChoices("HTTP_RETRIES"))
    backoff_factor: float = Field(0.5, validation_alias=AliasChoices("HTTP_BACKOFF"))

    # ערכים שמתעדכנים runtime, לא חוסמים ולידציה:
    spotify_user_access_token: str = Field("",  validation_alias=AliasChoices("SPOTIFY_USER_ACCESS_TOKEN"))
    spotify_user_expires_at: int   = Field(0,   validation_alias=AliasChoices("SPOTIFY_USER_EXPIRES_AT"))

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",     # נתיב מוחלט
        env_file_encoding="utf-8",
        extra="ignore",
    )
