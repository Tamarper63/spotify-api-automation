import os
from dotenv import load_dotenv
from infra.auth.oauth_handler import OAuthHandler

load_dotenv(override=True)

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
scopes = ["playlist-modify-public", "playlist-modify-private", "user-read-private"]

handler = OAuthHandler(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scopes=scopes
)

tokens = handler.authorize()

print("\n✅ Authorization complete.\n")
print("🔑 ACCESS TOKEN:\n", tokens["access_token"])
print("🔄 REFRESH TOKEN:\n", tokens.get("refresh_token", "<Not returned – use existing>"))
print("⏳ EXPIRES IN (sec):", tokens.get("expires_in"))
