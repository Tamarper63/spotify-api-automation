import time
from infra.config.loader import load_config
from infra.config.runtime_env_writer import update_runtime_env
from infra.auth.oauth_handler import OAuthHandler
from infra.auth.token_provider import get_token_response


class TokenManager:
    _token = None
    _expires_at = 0

    @classmethod
    def get_token(cls) -> str:
        now = time.time()
        if cls._token is None or now >= cls._expires_at:
            response = get_token_response()
            cls._token = response["access_token"]
            cls._expires_at = now + response["expires_in"] - 5
        return cls._token

    @staticmethod
    def get_user_token() -> str:
        config = load_config()

        access_token = config.spotify_user_access_token
        expires_at = int(config.spotify_user_expires_at or "0")

        if not access_token or time.time() > expires_at:
            refresh_token = config.spotify_refresh_token
            if not refresh_token:
                raise Exception("Missing refresh token in config")

            handler = OAuthHandler(
                client_id=config.client_id,
                client_secret=config.client_secret,
                redirect_uri=config.spotify_redirect_uri,
                scopes=[
                    "playlist-modify-public",
                    "playlist-modify-private",
                    "user-read-private",
                ],
            )
            tokens = handler.refresh_user_token(refresh_token)
            access_token = tokens["access_token"]
            expires_at = int(time.time()) + tokens.get("expires_in", 3600)

            update_runtime_env("SPOTIFY_USER_ACCESS_TOKEN", access_token)
            update_runtime_env("SPOTIFY_USER_EXPIRES_AT", str(expires_at))

        return access_token
