import base64
import requests


def _encode_client_credentials(client_id: str, client_secret: str) -> str:
    credentials = f"{client_id}:{client_secret}"
    return base64.b64encode(credentials.encode()).decode()


def get_token_response(client_id: str, client_secret: str, raw: bool = False) -> dict:
    """
    Requests a Spotify access token using client credentials flow.

    Args:
        client_id (str): Spotify Client ID
        client_secret (str): Spotify Client Secret
        raw (bool): If True, return full response object. Default: False

    Returns:
        dict or requests.Response: Access token JSON or full response
    """
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {_encode_client_credentials(client_id, client_secret)}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response if raw else response.json()
