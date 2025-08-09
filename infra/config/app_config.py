# infra/config/models.py (או היכן שמוגדר AppConfig)

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    # --- Spotify / HTTP ---
    client_id: str = Field(..., alias="SPOTIFY_CLIENT_ID")
    client_secret: str = Field(..., alias="SPOTIFY_CLIENT_SECRET")
    token_url: str = Field("https://accounts.spotify.com/api/token", alias="SPOTIFY_TOKEN_URL")
    base_url: str = Field("https://api.spotify.com/v1", alias="SPOTIFY_BASE_URL")

    timeout: float = Field(10.0, alias="TIMEOUT")               # תואם RequestHandler (float)
    retries: int = Field(3, alias="HTTP_RETRIES")               # חדש: קונפיג ל־_send_request
    backoff_factor: float = Field(0.5, alias="HTTP_BACKOFF")    # חדש: קונפיג ל־_send_request

    env_name: str = Field("local", alias="ENV_NAME")
    user_access_token_ext: str = Field("", alias="USER_ACCESS_TOKEN_EXT")
    spotify_redirect_uri: str = Field(..., alias="SPOTIFY_REDIRECT_URI")
    default_playlist_id: str = Field(..., alias="DEFAULT_PLAYLIST_ID")
    spotify_refresh_token: str = Field(..., alias="SPOTIFY_REFRESH_TOKEN")
    spotify_user_access_token: str = Field("", alias="SPOTIFY_USER_ACCESS_TOKEN")
    spotify_user_expires_at: str = Field("0", alias="SPOTIFY_USER_EXPIRES_AT")


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",   # פותר ValidationError על שדות נוספים כמו llm_provider
    )
