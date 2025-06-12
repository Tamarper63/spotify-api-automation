
import requests
import time
from typing import Optional, Dict, Any, Union


def _send_request(
    url: str,
    method: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Union[Dict[str, Any], str]] = None,
    json: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: int = 10
) -> requests.Response:
    """
    Sends an HTTP request with performance tracking and exception handling.
    """
    method = method.upper()
    headers = headers or {"Content-Type": "application/json"}

    start_time = time.time()
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            files=files,
            timeout=timeout
        )
        response.request_duration = (time.time() - start_time) * 1000  # in milliseconds
        return response

    except requests.RequestException as e:
        raise RuntimeError(f"[ERROR] {method} {url} failed: {e}") from e
