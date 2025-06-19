import requests
import time
import pytest
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
    Sends an HTTP request with performance tracking and logs for pytest-html reporting.
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
        duration_ms = int((time.time() - start_time) * 1000)
        response.request_duration = duration_ms

        # Log for HTML report
        log_entry = (
            f"{method} {url}"
            f"\n⏱ {duration_ms} ms"
            f" | 🔢 Status: {response.status_code}"
            f" | 📦 Size: {len(response.content)} bytes"
        )
        node = getattr(pytest, "current_test_node", {})
        node.setdefault("perf_logs", []).append(log_entry)
        pytest.current_test_node = node

        return response

    except requests.RequestException as e:
        raise RuntimeError(f"[ERROR] {method} {url} failed: {e}") from e
