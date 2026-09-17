"""
Test: Browser Compatibility — Login hoạt động trên Chrome, Firefox, Safari, Edge
Test Cases: feat_005 ac_001, ac_002
Feature: Browser Compatibility (feat_005)
Layer: cross_browser

Run with different browsers:
    pytest --browser=chromium
    pytest --browser=firefox
    pytest --browser=webkit  (Safari)

FAIL if: login không hoạt động trên bất kỳ browser nào → CROSS-BROWSER BUG.
"""
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.settings import CFG


class TestCrossBrowserLogin:
    """AC-001/002: Login hoạt động trên tất cả browsers (latest versions)"""

    @pytest.mark.cross_browser
    def test_login_form_renders_all_browsers(self, page: Page):
        """Login form renders correctly on any browser.

        FAIL if: form elements missing on a specific browser → CROSS-BROWSER UI BUG.
        """
        login_page = LoginPage(page).navigate()
        login_page.expect_form_visible()

    @pytest.mark.cross_browser
    def test_login_success_all_browsers(self, page: Page):
        """Successful login works across all browsers.

        FAIL if: login fails on a specific browser → AUTH FLOW BUG.
        """
        login_page = LoginPage(page).navigate()
        login_page.login(CFG.valid_username, CFG.valid_password)
        dashboard_page = DashboardPage(page)
        dashboard_page.expect_dashboard_loaded()

    @pytest.mark.cross_browser
    def test_login_failure_all_browsers(self, page: Page):
        """Error messages display correctly across all browsers.

        FAIL if: error message missing/incorrect on a specific browser → UI BUG.
        """
        login_page = LoginPage(page).navigate()
        login_page.login(CFG.nonexistent_username, "TestPass123!")
        login_page.expect_error_message("Your username is invalid!")
        login_page.expect_still_on_login_page()

    @pytest.mark.cross_browser
    def test_password_masked_all_browsers(self, page: Page):
        """Password masking works across all browsers.

        FAIL if: password not masked on a specific browser → SECURITY BUG.
        """
        login_page = LoginPage(page).navigate()
        login_page.fill_password("TestPass123!")
        login_page.expect_password_masked()