from requests import Response

from infra.http.request_sender import _send_request


class RequestHandler:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.spotify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", self.headers)
        return _send_request(
            url=url,
            method=method,
            headers=headers,
            **kwargs
        )

    def get(self, endpoint: str, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, url: str, *, json=None, **kwargs) -> Response:
        return self._request("DELETE", url, json=json, **kwargs)

    def patch(self, endpoint: str, **kwargs):
        return self._request("PATCH", endpoint, **kwargs)
