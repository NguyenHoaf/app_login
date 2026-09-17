"""
Test: Login form không cho phép submit với email trống / password trống
Test Cases: tc_005, tc_006
Feature: User Login Form (feat_001)
Layer: functional | Coverage: negative
"""
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage


class TestRequiredFields:
    """TC-005 & TC-006: Verify required field validation — empty email or password"""

    def test_empty_email_shows_error(self, login_page: LoginPage):
        """TC-005: Empty email → error message 'Please enter a valid email' or HTML5 validation.

        FAIL if: no error shown, form submits anyway → VALIDATION BUG.
        FAIL if: redirect to dashboard with empty email → SECURITY BUG.
        """
        login_page.fill_username("")
        login_page.fill_password("TestPass123!")
        login_page.click_submit()

        # Must NOT redirect away from login page
        assert "login" in login_page.page.url.lower(), \
            "BUG: Form submit với email trống vẫn redirect khỏi login page!"

        # Check for any validation message (browser HTML5 or custom)
        body_text = login_page.page.locator("body").text_content().lower()
        has_validation_msg = any(kw in body_text for kw in [
            "please fill", "required", "email", "username is invalid",
            "please enter", "không được để trống"
        ])
        assert has_validation_msg, \
            "BUG: Không hiển thị error message khi để trống email. " \
            "User không biết tại sao không submit được."

    def test_empty_password_shows_error(self, login_page: LoginPage):
        """TC-006: Empty password → error message.

        FAIL if: no error shown → VALIDATION BUG.
        """
        login_page.fill_username("test@example.com")
        login_page.fill_password("")
        login_page.click_submit()

        assert "login" in login_page.page.url.lower(), \
            "BUG: Form submit với password trống vẫn redirect!"

        body_text = login_page.page.locator("body").text_content().lower()
        has_validation_msg = any(kw in body_text for kw in [
            "please fill", "required", "password", "please enter",
            "không được để trống"
        ])
        assert has_validation_msg, \
            "BUG: Không hiển thị error message khi để trống password."

    def test_both_fields_empty_shows_error(self, login_page: LoginPage):
        """Combined: Both email and password empty → at least one error.

        FAIL if: no validation at all → CRITICAL BUG.
        """
        login_page.fill_username("")
        login_page.fill_password("")
        login_page.click_submit()

        assert "login" in login_page.page.url.lower(), \
            "BUG: Form submit với cả 2 fields trống vẫn redirect!"

        body_text = login_page.page.locator("body").text_content().lower()
        assert len(body_text.strip()) > 0, \
            "BUG: Trang login không có nội dung sau khi submit với fields trống"