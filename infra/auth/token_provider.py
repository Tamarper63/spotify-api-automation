import base64
import requests
from infra.config.loader import load_config


def _encode_client_credentials(client_id: str, client_secret: str) -> str:
    credentials = f"{client_id}:{client_secret}"
    return base64.b64encode(credentials.encode()).decode()


def get_token_response(raw: bool = False) -> dict:
    config = load_config()
    token_url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {_encode_client_credentials(config.client_id, config.client_secret)}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response if raw else response.json()
