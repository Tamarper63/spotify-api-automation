# infra/utils/log_utils.py

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

    try:
        # צור מבנה לוג אם לא קיים
        node = getattr(pytest, "current_test_node", {})
        node.setdefault("perf_logs", []).append(entry)
        pytest.current_test_node = node
    except Exception as e:
        # fallback – אפשרות לדפדוף STDOUT (אם נדרש)
        print(f"[log fallback] {entry}")
