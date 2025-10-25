# tools/bootstrap_oauth.py
from pathlib import Path
import os, json, time, tempfile
from dotenv import load_dotenv, find_dotenv
from infra.auth.oauth_handler import OAuthHandler

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"

load_dotenv(find_dotenv(usecwd=False), override=False)

handler = OAuthHandler(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scopes=["playlist-modify-public","playlist-modify-private","user-read-private"],
)

tokens = handler.authorize()
access = tokens["access_token"]
refresh = tokens.get("refresh_token")
expires_in = tokens.get("expires_in")
expires_at = int(time.time()) + int(expires_in) if expires_in else tokens.get("expires_at", 0)

kv = {
    "SPOTIFY_USER_ACCESS_TOKEN": access,
    "SPOTIFY_USER_EXPIRES_AT": str(expires_at),
}
if refresh:
    kv["SPOTIFY_REFRESH_TOKEN"] = refresh

lines = {}
if ENV_PATH.exists():
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if raw.strip() and not raw.strip().startswith("#") and "=" in raw:
            k, v = raw.split("=", 1); lines[k] = v

lines.update(kv)
tmp = tempfile.NamedTemporaryFile("w", delete=False, dir=str(ENV_PATH.parent), encoding="utf-8")
with tmp as f:
    for k, v in lines.items():
        f.write(f"{k}={v}\n")
Path(tmp.name).replace(ENV_PATH)

print(json.dumps({"status": "ok", "updated_keys": list(kv.keys())}))
