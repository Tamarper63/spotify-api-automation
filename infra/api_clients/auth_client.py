# infra/api_clients/auth_client.py

import base64
from pydantic_core import ValidationError
from infra.http.request_sender import _send_request
from infra.config.settings import get_settings


class AuthClient:
    def __init__(self, client_id: str = None, client_secret: str = None):
        try:
            settings = get_settings()
            self.client_id = client_id or settings.spotify_client_id
            self.client_secret = client_secret or settings.spotify_client_secret
        except ValidationError as e:
            raise ValueError("Missing required credentials") from e

        self.token_url = "https://accounts.spotify.com/api/token"

    def get_token_response(self, raw: bool = False):
        headers = {
            "Authorization": f"Basic {self._encode_credentials()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        response = _send_request(
            url=self.token_url,
            method="POST",
            headers=headers,
            data=data
        )
        return response if raw else response.json()

    def _encode_credentials(self) -> str:
        auth_str = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(auth_str.encode()).decode()
