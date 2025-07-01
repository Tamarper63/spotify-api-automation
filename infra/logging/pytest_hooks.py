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
