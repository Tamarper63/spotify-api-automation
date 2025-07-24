import json
import pytest
import logging

logger = logging.getLogger("spotify_test")

def log_api_call(method: str, url: str, status_code: int, elapsed_ms: int, response_body=None):
    entry = f"{method} {url}\n⏱ {elapsed_ms} ms | 📦 Status: {status_code}"
    if response_body:
        try:
            formatted = json.dumps(response_body, indent=2, ensure_ascii=False)
            entry += f"\n📄 Response:\n{formatted}"
        except Exception:
            entry += f"\n📄 Response:\n{response_body}"

    if hasattr(pytest, "current_test_node"):
        pytest.current_test_node.setdefault("perf_logs", []).append(entry)
    else:
        print(f"[log fallback] {entry}")


def log_warning(message: str):
    """
    Log a warning outside the test node context (e.g., in conftest, setup, fixtures).
    """
    logger.warning(f"⚠️ {message}")
