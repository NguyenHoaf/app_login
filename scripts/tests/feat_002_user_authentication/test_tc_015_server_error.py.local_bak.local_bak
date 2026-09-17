"""
Test: Server error xử lý login — hiển thị error message
Test Case: tc_015
Feature: User Authentication Process (feat_002)
Layer: e2e | Coverage: error

Simulate server/db error via Playwright route interception,
then verify system handles it gracefully.
"""
import pytest
from playwright.sync_api import Page, Route
from pages.login_page import LoginPage
from config.settings import CFG


class TestServerError:
    """TC-015: Verify server error → friendly error message"""

    def test_api_500_during_login_shows_friendly_message(self, page: Page):
        """Simulate API 500 on form submit.

        FAIL if: browser crashes / chrome-error page → POOR ERROR HANDLING.
        FAIL if: no error message to user → UX BUG.
        FAIL if: app throws unhandled exception in UI → STABILITY BUG.
        """
        login_page = LoginPage(page).navigate()
        intercepted = []

        def intercept_submit(route: Route):
            intercepted.append(True)
            route.fulfill(
                status=500,
                content_type="text/html",
                body="<html><body>Internal Server Error</body></html>"
            )

        # Block the form POST action
        page.route("**/*", intercept_submit)

        login_page.fill_credentials(CFG.valid_username, CFG.valid_password)
        login_page.click_submit()

        # Verify the route was actually intercepted
        assert len(intercepted) > 0, \
            "BUG: Route interception không hoạt động — test infrastructure issue"

        # Must NOT show chrome-error:// page
        assert "chrome-error" not in page.url.lower(), \
            "BUG: Khi server trả về 500, app bị crash ra chrome-error page. " \
            "Cần xử lý lỗi graceful — hiển thị thông báo thân thiện thay vì crash trình duyệt."

        # Must show a friendly error or at least stay on login page
        assert "login" in page.url.lower() or "error" in page.url.lower(), \
            "BUG: Server 500 gây redirect đến trang không xác định. " \
            f"URL hiện tại: {page.url}"

        # Check for friendly error message
        body_text = page.locator("body").text_content().lower()
        friendly_keywords = [
            "try again", "please try", "error", "server",
            "unable", "something went wrong", "please try again later"
        ]
        has_friendly = any(kw in body_text for kw in friendly_keywords)
        assert has_friendly, \
            "BUG: Server trả về 500 nhưng không hiển thị thông báo lỗi thân thiện cho user. " \
            f"Body content: {body_text[:200]}..."

    def test_network_timeout_shows_friendly_message(self, page: Page):
        """Simulate network timeout during login.

        FAIL if: no graceful handling → UX BUG.
        """
        login_page = LoginPage(page).navigate()

        def abort_login(route: Route):
            route.abort("timedout")

        page.route("**/*", abort_login)

        login_page.fill_credentials(CFG.valid_username, CFG.valid_password)
        login_page.click_submit()

        # Verify graceful handling — not a crash
        assert "chrome-error" not in page.url.lower(), \
            "BUG: Network timeout gây crash trình duyệt (chrome-error page)."

        # Should at least show something to the user
        body_text = page.locator("body").text_content().lower()
        assert len(body_text.strip()) > 0, \
            "BUG: Network timeout → trang trắng, không có nội dung."