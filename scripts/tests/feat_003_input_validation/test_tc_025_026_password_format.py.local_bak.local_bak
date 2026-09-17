"""
Test: Password format — special characters & alphanumeric requirements
Test Cases: tc_025, tc_026
Feature: Input Validation Rules (feat_003)
Layer: functional | Coverage: negative
"""
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.settings import CFG


class TestPasswordSpecialChars:
    """TC-025: Password không chứa special characters → validation fail"""

    def test_password_no_special_chars_rejected(self, login_page: LoginPage):
        """Negative — only letters+numbers (10 chars), no special → MUST be rejected.

        Spec: Password requires alphanumeric + special characters.
        FAIL if: login succeeds with password lacking special chars → SECURITY BUG.
        """
        login_page.login(CFG.valid_username, "Password12345")

        # If redirected to dashboard → special-char policy NOT enforced → BUG
        is_logged_in = "logged-in-successfully" in login_page.page.url.lower() or \
                       "dashboard" in login_page.page.url.lower()
        assert not is_logged_in, \
            "BUG: Password policy (special characters) không được enforce! " \
            "'Password12345' (không special chars) vẫn login thành công. " \
            "Spec yêu cầu password phải chứa special characters."

        assert "login" in login_page.page.url.lower(), \
            "BUG: Submit với password thiếu special chars gây lỗi redirect lạ"


class TestPasswordAlphanumeric:
    """TC-026: Password không có cả chữ và số → validation fail"""

    def test_password_only_letters_rejected(self, login_page: LoginPage):
        """Negative — only letters + special, no digits → MUST be rejected.

        FAIL if: login succeeds → PASSWORD POLICY BYPASS.
        """
        login_page.login(CFG.valid_username, "PasswordABC!")

        is_logged_in = "logged-in-successfully" in login_page.page.url.lower() or \
                       "dashboard" in login_page.page.url.lower()
        assert not is_logged_in, \
            "BUG: Password 'PasswordABC!' (chỉ chữ + special, không số) vẫn login được. " \
            "Spec yêu cầu password phải chứa alphanumeric (cả chữ và số)."

    def test_password_only_digits_rejected(self, login_page: LoginPage):
        """Negative — only digits + special, no letters → MUST be rejected.

        FAIL if: login succeeds → PASSWORD POLICY BYPASS.
        """
        login_page.login(CFG.valid_username, "1234567890!")

        is_logged_in = "logged-in-successfully" in login_page.page.url.lower() or \
                       "dashboard" in login_page.page.url.lower()
        assert not is_logged_in, \
            "BUG: Password '1234567890!' (chỉ số + special, không chữ) vẫn login được. " \
            "Spec yêu cầu password phải chứa alphanumeric (cả chữ và số)."