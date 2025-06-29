import requests
import time
from typing import Optional, Dict, Any, Union
from utils.log_utils import log_api_call


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
    method = method.upper()
    headers = headers or {"Content-Type": "application/json"}

    try:
        start = time.perf_counter()
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
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        try:
            body = response.json()
        except Exception:
            body = response.text

        log_api_call(
            method=method,
            url=url,
            status_code=response.status_code,
            elapsed_ms=elapsed_ms,
            response_body=body
        )

        return response

    except requests.RequestException as e:
        raise RuntimeError(f"[ERROR] {method} {url} failed: {e}") from e
