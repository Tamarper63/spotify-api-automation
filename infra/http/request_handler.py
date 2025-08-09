# infra/http/request_handler.py

from __future__ import annotations
from typing import Any, Dict, Optional
import time

from infra.http.base_request_engine import _send_request
from utils.log_utils import log_api_call


class RequestHandler:
    """
    Single client-facing HTTP wrapper.
    - Builds absolute URL from base_url + endpoint
    - Injects Bearer token + default headers (Content-Type: application/json)
    - Delegates transport to _send_request (retries/backoff/timeout)
    - Centralizes structured logging via log_api_call
    - Keeps compatibility with verb-specific methods and adds a unified send()
    """

    def __init__(
        self,
        token: str,
        base_url: str = "https://api.spotify.com/v1",
        timeout: float = 10.0,
        retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.api_call_metrics = []

    # --- internal helpers ---

    def _prepare_headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = dict(custom_headers or {})
        headers.setdefault("Authorization", f"Bearer {self.token}")
        headers.setdefault("Content-Type", "application/json")
        return headers

    def _absolute_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _call(self, method: str, endpoint: str, **kwargs) -> Any:
        url = self._absolute_url(endpoint)
        # allow override via kwargs['headers']
        headers = self._prepare_headers(kwargs.pop("headers", None))

        start = time.perf_counter()
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
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        try:
            # log_api_call(method, url, status_code, elapsed_ms, response_body)
            log_api_call(method, url, response.status_code, elapsed_ms, response.text)
        except Exception:
            # do not fail request flow due to logging issues
            pass

        self.api_call_metrics.append((method, endpoint, response.status_code))
        return response

    # --- unified entry point used by SpotifyClient ---

    def send(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Compatibility shim for unified calling style.
        SpotifyClient uses this entry to avoid coupling to verb methods.
        """
        if not method:
            raise ValueError("HTTP method is required")
        return self._call(method.upper(), endpoint, **kwargs)

    # --- verb-specific helpers (kept for backward compatibility) ---

    def get(self, endpoint: str, **kwargs) -> Any:
        return self._call("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Any:
        return self._call("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Any:
        return self._call("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Any:
        return self._call("DELETE", endpoint, **kwargs)
