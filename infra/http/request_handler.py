
from infra.http.request_sender import _send_request


class RequestHandler:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.spotify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str, params=None):
        url = f"{self.base_url}{endpoint}"
        return _send_request(
            url=url,
            method="GET",
            headers=self.headers,
            params=params
        )

    def post(self, endpoint: str, json=None):
        url = f"{self.base_url}{endpoint}"
        return _send_request(
            url=url,
            method="POST",
            headers=self.headers,
            json=json
        )

    def put(self, endpoint: str, json=None, data=None, custom_headers=None):
        url = f"{self.base_url}{endpoint}"
        headers = custom_headers if custom_headers else self.headers
        return _send_request(
            url=url,
            method="PUT",
            headers=headers,
            json=json,
            data=data
        )

    def delete(self, endpoint: str, json=None):
        url = f"{self.base_url}{endpoint}"
        return _send_request(
            url=url,
            method="DELETE",
            headers=self.headers,
            json=json
        )

    def delete_with_body(self, endpoint: str, json=None):
        url = f"{self.base_url}{endpoint}"
        return _send_request(
            url=url,
            method="DELETE",
            headers=self.headers,
            json=json
        )

