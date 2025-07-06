import base64
import requests
from infra.config.settings import get_settings


def _encode_client_credentials(client_id: str, client_secret: str) -> str:
    credentials = f"{client_id}:{client_secret}"
    return base64.b64encode(credentials.encode()).decode()


def get_token_response(raw: bool = False) -> dict:
    settings = get_settings()
    token_url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {_encode_client_credentials(settings.spotify_client_id, settings.spotify_client_secret)}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response if raw else response.json()
