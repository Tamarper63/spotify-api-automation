import json

import pytest


def log_api_call(method: str, url: str, status_code: int, elapsed_ms: int, response_body=None):
    entry = f"{method} {url}\n⏱ {elapsed_ms} ms | 📦 Status: {status_code}"
    if response_body:
        try:
            formatted = json.dumps(response_body, indent=2, ensure_ascii=False)
            entry += f"\n📄 Response:\n{formatted}"
        except Exception:
            entry += f"\n📄 Response:\n{response_body}"

    # Write to pytest runtime log
    if hasattr(pytest, "current_test_node"):
        pytest.current_test_node.setdefault("perf_logs", []).append(entry)
    else:
        # Fallback: temporary store in file or local context (for debugging only)
        print(f"[log fallback] {entry}")
