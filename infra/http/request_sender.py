import requests
import time
import pytest
import json
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
    Sends an HTTP request with timing and logging for pytest-html.
    """
    method = method.upper()
    headers = headers or {"Content-Type": "application/json"}

    start_time = time.perf_counter()
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
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        response.request_duration = duration_ms

        # Try to extract response body
        try:
            body = response.json()
            body_str = json.dumps(body, indent=2, ensure_ascii=False)
        except Exception:
            body_str = response.text

        # Build log entry
        log_entry = (
            f"{method} {url}\n"
            f"⏱ {duration_ms} ms | 🔢 Status: {response.status_code} | 📦 Size: {len(response.content)} bytes"
            f"\n📄 Response:\n{body_str}"
        )

        # Store in current test node
        node = getattr(pytest, "current_test_node", {})
        node.setdefault("perf_logs", []).append(log_entry)
        pytest.current_test_node = node

        return response

    except requests.RequestException as e:
        raise RuntimeError(f"[ERROR] {method} {url} failed: {e}") from e
