from infra.config.loader import load_config
from infra.auth.oauth_handler import OAuthHandler


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

    print("\n✅ Access Token:", tokens["access_token"])
    print("🔁 Refresh Token:", tokens.get("refresh_token", "(not returned)"))
    print("⏳ Expires In:", tokens.get("expires_in", "unknown"), "seconds")


if __name__ == "__main__":
    main()
