import time
from infra.config.loader import load_config
from infra.auth.oauth_handler import OAuthHandler
from infra.config.runtime_env_writer import update_runtime_env


def main():
    config = load_config()

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

    tokens = handler.authorize()

    update_runtime_env("SPOTIFY_USER_ACCESS_TOKEN", tokens["access_token"])
    update_runtime_env("SPOTIFY_REFRESH_TOKEN", tokens["refresh_token"])
    update_runtime_env(
        "SPOTIFY_USER_EXPIRES_AT", str(int(time.time()) + tokens.get("expires_in", 3600))
    )

    print("✅ Tokens written to .runtime.env")


if __name__ == "__main__":
    main()
