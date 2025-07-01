import pytest


def pytest_runtest_logstart(nodeid, location):
    pytest.current_test_node = {"perf_logs": []}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        logs = getattr(pytest, "current_test_node", {}).get("perf_logs", [])
        if logs:
            report.sections.append(("API Requests", "\n".join(logs)))

        client = item.funcargs.get("spotify_user_client") or item.funcargs.get("spotify_client")
        if client and hasattr(client, "request_handler") and hasattr(client.request_handler, "api_call_metrics"):
            metrics = client.request_handler.api_call_metrics
            if metrics:
                lines = [f"{m['method']} {m['url']} took {m['duration_sec']:.3f}s (status {m['status_code']})" for m in
                         metrics]
                report.sections.append(("API Call Metrics", "\n".join(lines)))
                client.request_handler.api_call_metrics.clear()
