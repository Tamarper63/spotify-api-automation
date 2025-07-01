from requests import Response
import time

from infra.http.request_sender import _send_request


class RequestHandler:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.spotify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.api_call_metrics = []

    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", self.headers)

        start_time = time.perf_counter()
        response = _send_request(
            url=url,
            method=method,
            headers=headers,
            **kwargs
        )
        duration = time.perf_counter() - start_time

        self.api_call_metrics.append({
            "method": method,
            "url": url,
            "duration_sec": duration,
            "status_code": response.status_code,
        })

        return response

    def get(self, endpoint: str, **kwargs) -> Response:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Response:
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, *, json=None, **kwargs) -> Response:
        return self._request("DELETE", endpoint, json=json, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response:
        return self._request("PATCH", endpoint, **kwargs)
