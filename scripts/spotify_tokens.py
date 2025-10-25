#!/usr/bin/env python3
# python tools/spotify_tokens.py bootstrap

from __future__ import annotations
import argparse, os, json, time, tempfile, sys
from pathlib import Path
from infra.config.loader import load_config
from infra.auth.oauth_handler import OAuthHandler

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
DEFAULT_SCOPES = ["playlist-modify-public","playlist-modify-private","user-read-private"]

def _oauth_handler(scopes):
    cfg = load_config()  # AppConfig עם validation_alias ו-env_file מוחלט
    return OAuthHandler(
        client_id=cfg.client_id,
        client_secret=cfg.client_secret,
        redirect_uri=cfg.spotify_redirect_uri,
        scopes=scopes or DEFAULT_SCOPES,
    )

def _authorize(scopes):
    return _oauth_handler(scopes).authorize()

def _update_env_atomic(updates: dict, env_path: Path = ENV_PATH) -> None:
    lines = {}
    if env_path.exists():
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            if raw and not raw.startswith("#") and "=" in raw:
                k, v = raw.split("=", 1); lines[k] = v
    lines.update(updates)
    tmp = tempfile.NamedTemporaryFile("w", delete=False, dir=str(env_path.parent), encoding="utf-8")
    with tmp as f:
        for k, v in lines.items():
            f.write(f"{k}={v}\n")
    Path(tmp.name).replace(env_path)

def cmd_bootstrap(args):
    t = _authorize(args.scopes)
    access = t["access_token"]
    refresh = t.get("refresh_token")
    expires_in = t.get("expires_in")
    expires_at = int(time.time()) + int(expires_in) if expires_in else int(t.get("expires_at", 0))
    updates = {"SPOTIFY_USER_ACCESS_TOKEN": access, "SPOTIFY_USER_EXPIRES_AT": str(expires_at)}
    if refresh:
        updates["SPOTIFY_REFRESH_TOKEN"] = refresh
    _update_env_atomic(updates, ENV_PATH)
    print(json.dumps({"status": "ok", "updated": list(updates.keys())}))

def cmd_show(args):
    t = _authorize(args.scopes)
    out = {
        "access_token": t.get("access_token"),
        "refresh_token": t.get("refresh_token", "(not returned)"),
        "expires_in": t.get("expires_in", "unknown"),
    }
    print(json.dumps(out, indent=2))

def main():
    p = argparse.ArgumentParser(prog="spotify_tokens", description="Authorize and manage Spotify user tokens")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("bootstrap", help="Authorize and write tokens to .env")
    b.add_argument("--scopes", nargs="*", default=DEFAULT_SCOPES)
    b.set_defaults(func=cmd_bootstrap)

    s = sub.add_parser("show", help="Authorize and print tokens only")
    s.add_argument("--scopes", nargs="*", default=DEFAULT_SCOPES)
    s.set_defaults(func=cmd_show)

    args = p.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
