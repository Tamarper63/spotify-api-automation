import os
import time
from dotenv import load_dotenv
from infra.auth.oauth_handler import OAuthHandler


def update_dotenv(key: str, value: str):
    env_path = ".env"
    lines = []
    found = False
    if os.path.exists(env_path):
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


# Load environment variables
load_dotenv()

# Create the handler
handler = OAuthHandler(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scopes=["playlist-modify-public", "playlist-modify-private", "user-read-private"],
)

# Start authorization and get tokens
tokens = handler.authorize()

# Save all needed info to .env
update_dotenv("SPOTIFY_USER_ACCESS_TOKEN", tokens["access_token"])
update_dotenv("SPOTIFY_REFRESH_TOKEN", tokens["refresh_token"])
update_dotenv("SPOTIFY_USER_EXPIRES_AT", str(int(time.time()) + tokens["expires_in"]))

print("✅ Tokens successfully written to .env")
