# api_clients/auth_client.py

import base64
import requests
from dotenv import load_dotenv
from infra.http.config_manager import ConfigManager

load_dotenv()  # Load SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET from .env


class AuthClient:
    def __init__(self):
        self.client_id = ConfigManager.get_client_id()
        self.client_secret = ConfigManager.get_client_secret()
        self.token_url = "https://accounts.spotify.com/api/token"

    def get_access_token(self) -> str:
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_header = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials"
        }

        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
