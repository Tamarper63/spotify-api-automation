# infra/request_handler.py

from typing import Optional, Dict, Any
from infra.request_sender import _send_request  # ✅ IMPORT HERE


class RequestHandler:
    """
    High-level HTTP handler that wraps the raw _send_request function
    and manages auth headers per request.
    """
    def __init__(self, token: str):
        self.token = token

    def _build_headers(self, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def get(self, url: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        return _send_request(                       # ✅ USED HERE
            url=url,
            method="GET",
            headers=self._build_headers(headers),
            params=params,
            timeout=timeout
        )

    def post(self, url: str, json: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        return _send_request(                       # ✅ USED HERE
            url=url,
            method="POST",
            headers=self._build_headers(headers),
            json=json,
            timeout=timeout
        )

    def put(self, url: str, json: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        return _send_request(                       # ✅ USED HERE
            url=url,
            method="PUT",
            headers=self._build_headers(headers),
            json=json,
            timeout=timeout
        )

    def delete(self, url: str,
               headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        return _send_request(                       # ✅ USED HERE
            url=url,
            method="DELETE",
            headers=self._build_headers(headers),
            timeout=timeout
        )
