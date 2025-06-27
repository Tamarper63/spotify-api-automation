import os
import time

from infra.api_clients.spotify_client import SpotifyClient
from infra.auth.oauth_handler import OAuthHandler


def update_dotenv(key: str, value: str):
    from pathlib import Path
    env_path = Path(".env")
    lines = []
    found = False

    if not env_path.exists():
        env_path.touch()

    with open(env_path, "r") as f:
        for line in f:
            if line.startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                found = True
            else:
                lines.append(line)

    if not found:
        lines.append(f"{key}={value}\n")

    with open(env_path, "w") as f:
        f.writelines(lines)


class TokenManager:
    _token = None
    _expires_at = 0

    @classmethod
    def get_token(cls) -> str:
        now = time.time()
        if cls._token is None or now >= cls._expires_at:
            auth_client = SpotifyClient()
            response = auth_client.get_token_response()
            cls._token = response["access_token"]
            cls._expires_at = now + response["expires_in"] - 5  # buffer
        return cls._token

    @staticmethod
    def get_user_token() -> str:
        access_token = os.getenv("SPOTIFY_USER_ACCESS_TOKEN")
        expires_at = int(os.getenv("SPOTIFY_USER_EXPIRES_AT", "0"))

        if not access_token or time.time() > expires_at:
            print("🔄 Token expired — refreshing...")
            refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
            if not refresh_token:
                raise Exception("Missing refresh token in .env")

            handler = OAuthHandler(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                scopes=["playlist-modify-public", "playlist-modify-private", "user-read-private"]
            )
            tokens = handler.refresh_user_token(refresh_token)

            access_token = tokens["access_token"]
            update_dotenv("SPOTIFY_USER_ACCESS_TOKEN", access_token)

            # Save expiry time if provided
            if "expires_in" in tokens:
                expires_at = int(time.time()) + tokens["expires_in"]
                update_dotenv("SPOTIFY_USER_EXPIRES_AT", str(expires_at))

        return access_token
