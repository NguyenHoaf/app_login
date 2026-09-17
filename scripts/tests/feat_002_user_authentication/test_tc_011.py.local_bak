"""
Test: Đăng nhập thành công với email và password hợp lệ
Test Case: tc_011
Feature: User Authentication Process (feat_002)
Layer: e2e | Coverage: happy
"""
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.settings import CFG


class TestLoginSuccess:
    """TC-011: Verify user đăng nhập thành công với email và password đúng"""

    def test_login_success(self, login_page: LoginPage, dashboard_page: DashboardPage):
        """Happy path — valid credentials → redirect to dashboard."""

        # Steps 1-3: Navigate, fill credentials, submit
        login_page.login(CFG.valid_username, CFG.valid_password)

        # Step 4: Verify redirect và session
        dashboard_page.expect_dashboard_loaded()

        # Additional: logout works
        dashboard_page.click_logout()
        login_page.expect_form_visible()