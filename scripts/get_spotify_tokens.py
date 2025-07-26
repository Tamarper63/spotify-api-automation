import os
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

    # Safe CLI output block
    output = [
        f"\n✅ Access Token: {tokens['access_token']}",
        f"🔁 Refresh Token: {tokens.get('refresh_token', '(not returned)')}",
        f"⏳ Expires In: {tokens.get('expires_in', 'unknown')} seconds",
    ]

    for line in output:
        print(line)


if __name__ == "__main__":
    main()
