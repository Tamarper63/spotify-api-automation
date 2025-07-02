import logging
import time
from typing import Optional
import requests
from requests import Response, RequestException

logger = logging.getLogger(__name__)


def _send_request(
        url: str,
        method: str,
        headers: dict,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
        timeout: float = 10.0,
        retries: int = 3,
        backoff_factor: float = 0.5,
) -> Response:
    """
    Send HTTP request with retry and timeout.

    Args:
        url: Full request URL.
        method: HTTP method.
        headers: HTTP headers.
        params: Query parameters.
        json: JSON body.
        data: Form data.
        timeout: Timeout in seconds for each request.
        retries: Number of retries on recoverable errors.
        backoff_factor: Backoff multiplier for retries.

    Returns:
        requests.Response object.

    Raises:
        RequestException on repeated failures.
    """
    attempt = 0
    while attempt <= retries:
        try:
            logger.debug(f"Sending request {method} {url}, attempt {attempt + 1}")
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
                data=data,
                timeout=timeout,
            )

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                wait_time = float(retry_after) if retry_after else (backoff_factor * (2 ** attempt))
                logger.warning(f"Rate limited on attempt {attempt + 1}, retrying after {wait_time} seconds")
                time.sleep(wait_time)
                attempt += 1
                continue

            # Retry on 5xx server errors
            if 500 <= response.status_code < 600:
                wait_time = backoff_factor * (2 ** attempt)
                logger.warning(
                    f"Server error {response.status_code} on attempt {attempt + 1}, retrying after {wait_time} seconds")
                time.sleep(wait_time)
                attempt += 1
                continue

            return response

        except (requests.Timeout, requests.ConnectionError) as exc:
            wait_time = backoff_factor * (2 ** attempt)
            logger.warning(f"Request exception on attempt {attempt + 1}: {exc}. Retrying after {wait_time} seconds")
            time.sleep(wait_time)
            attempt += 1

    logger.error(f"Failed to complete request {method} {url} after {retries + 1} attempts")
    raise RequestException(f"Failed request after {retries + 1} attempts: {method} {url}")
