import base64


def encode_client_credentials(client_id: str, client_secret: str) -> str:
    """
    Return Base64-encoded client_id:client_secret for Authorization header.
    """
    return base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
