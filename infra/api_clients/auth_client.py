import base64

import requests
from pydantic import ValidationError
from infra.config.settings import get_settings


class AuthClient:
    def __init__(self):
        try:
            settings = get_settings()
            self.client_id = settings.spotify_client_id
            self.client_secret = settings.spotify_client_secret
        except ValidationError as e:
            raise ValueError("Missing required credentials") from e

        self.token_url = "https://accounts.spotify.com/api/token"

    def get_token_response(self, raw: bool = False):
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

        if raw:
            return response

        return response.json()

    @staticmethod
    def post_token_request_raw(url: str, headers: dict, data: dict) -> requests.Response:
        return requests.post(url, headers=headers, data=data)
