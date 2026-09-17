"""
Auto-attach screenshot when a test fails — hooks into pytest_runtest_makereport.

Usage: add to conftest.py or enable via pytest_configure.
"""
import pathlib
from datetime import datetime

import pytest
from playwright.sync_api import Page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and attach to the report."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Locate the page fixture if available
        page = item.funcargs.get("page")
        if page is None:
            # Check for self.page in class-based tests
            for fixt in item.funcargs.values():
                if isinstance(fixt, Page):
                    page = fixt
                    break

        if page:
            screenshot_dir = pathlib.Path("test_output/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{item.nodeid.replace('::', '_')}_{timestamp}.png"
            filepath = screenshot_dir / filename
            page.screenshot(path=str(filepath))
            # Attach to the HTML report
            if hasattr(report, "extra"):
                report.extra.append(pytest.extras.image(str(filepath)))
            else:
                print(f"\n[Screenshot saved] {filepath}")