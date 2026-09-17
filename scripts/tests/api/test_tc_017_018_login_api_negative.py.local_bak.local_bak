"""
Test: API — POST /api login positive & negative
Test Cases: tc_017, tc_018
Feature: User Authentication Process (feat_002)
Layer: api | Coverage: happy, negative

Note: Uses Playwright browser to login (practice site blocks raw requests).
"""
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.settings import CFG


class TestLoginApiSuccess:
    """TC-017: Đăng nhập thành công qua browser — verify redirect + session"""

    def test_login_success_browser(self, login_page: LoginPage, dashboard_page: DashboardPage):
        """Happy path — login via browser, verify redirect + dashboard content."""
        login_page.login(CFG.valid_username, CFG.valid_password)
        dashboard_page.expect_dashboard_loaded()


class TestLoginApiNegative:
    """TC-018: Đăng nhập thất bại — kiểm tra error message & status"""

    def test_login_nonexistent_user_browser(self, login_page: LoginPage):
        """Negative — nonexistent username → error message, no redirect."""
        login_page.login(CFG.nonexistent_username, "TestPass123!")
        login_page.expect_error_message("Your username is invalid!")
        login_page.expect_still_on_login_page()

    def test_login_wrong_password_browser(self, login_page: LoginPage):
        """Negative — valid user, wrong password → error message."""
        login_page.login(CFG.valid_username, CFG.wrong_password)
        login_page.expect_error_message("Your password is invalid!")
        login_page.expect_still_on_login_page()