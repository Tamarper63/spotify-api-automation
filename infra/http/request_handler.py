from infra.http.base_request_engine import _send_request
from utils.log_utils import log_api_call


class RequestHandler:
    def __init__(
        self,
        token: str,
        base_url: str = "https://api.spotify.com/v1",
        timeout: float = 10.0,
        retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        self.token = token
        self.base_url = base_url
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.api_call_metrics = []

    def _prepare_headers(self, custom_headers=None):
        headers = custom_headers.copy() if custom_headers else {}
        headers.setdefault("Authorization", f"Bearer {self.token}")
        headers.setdefault("Content-Type", "application/json")
        return headers

    def _call(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = self._prepare_headers(kwargs.pop("headers", {}))

        response = _send_request(
            url=url,
            method=method,
            headers=headers,
            params=kwargs.get("params"),
            json=kwargs.get("json"),
            data=kwargs.get("data"),
            timeout=self.timeout,
            retries=self.retries,
            backoff_factor=self.backoff_factor,
        )

        log_api_call(method, url, response.status_code, int(response.elapsed.total_seconds() * 1000), response.text)
        self.api_call_metrics.append((method, endpoint, response.status_code))
        return response

    def get(self, endpoint: str, **kwargs):
        return self._call("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._call("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self._call("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._call("DELETE", endpoint, **kwargs)
