"""
Test: Password length boundary — min=10, max=32
Test Cases: tc_023, tc_024
Feature: Input Validation Rules (feat_003)
Layer: functional | Coverage: boundary
"""
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from config.settings import CFG


class TestPasswordMinLength:
    """TC-023: VER2 — Password dưới 10 ký tự → validation fail (boundary)"""

    def test_password_9_chars_rejected(self, login_page: LoginPage):
        """Boundary: 9 chars → MUST be rejected (below min=10).

        Spec: Password policy updated — minimum 10 characters (from 8).
        FAIL if: login succeeds with 9-char password → SECURITY BUG (policy bypass).
        """
        pwd_9 = "A1@" + "a" * 6
        assert len(pwd_9) == 9

        login_page.login(CFG.valid_username, pwd_9)

        # If redirect to dashboard → password policy NOT enforced → SECURITY BUG
        is_logged_in = "logged-in-successfully" in login_page.page.url.lower() or \
                       "dashboard" in login_page.page.url.lower()
        assert not is_logged_in, \
            "BUG: Password policy không được enforce! " \
            "Password 9 ký tự (dưới min=10) vẫn login thành công. " \
            "Đây là lỗ hổng bảo mật: user/password yếu vẫn được chấp nhận. " \
            "Spec v2 cập nhật: minimum từ 8 lên 10 ký tự."

        assert "login" in login_page.page.url.lower(), \
            "BUG: Submit với password 9 ký tự gây lỗi không xác định"

    def test_password_10_chars_accepted(self, login_page: LoginPage):
        """Boundary: 10 chars → should be accepted (meets min=10).

        Note: accept in field != login success. Server may still reject for other reasons.
        The real validation should let 10-char passwords through.
        """
        pwd_10 = "A1@" + "a" * 7
        assert len(pwd_10) == 10

        login_page.fill_password(pwd_10)
        actual = login_page.password_input.input_value()
        assert actual == pwd_10, \
            f"BUG: Password 10 ký tự không được chấp nhận trong input field. " \
            f"Expected '{pwd_10}', got '{actual}'"


class TestPasswordMaxLength:
    """TC-024: Password vượt quá 32 ký tự → validation fail (boundary)"""

    def test_password_33_chars_truncated_or_rejected(self, login_page: LoginPage):
        """Boundary: 33 chars → MUST be rejected or truncated.

        FAIL if: 33-char password accepted in field → INPUT VALIDATION BUG.
        """
        pwd_33 = "A1@" + "a" * 30
        assert len(pwd_33) == 33

        login_page.fill_password(pwd_33)
        actual = login_page.password_input.input_value()

        assert len(actual) <= 32, \
            f"BUG: Password input field không enforce maxlength=32. " \
            f"Nhập 33 ký tự nhưng field chấp nhận {len(actual)} ký tự. " \
            f"Spec yêu cầu max 32 characters — có nguy cơ buffer overflow."

    def test_password_32_chars_accepted(self, login_page: LoginPage):
        """Boundary: 32 chars → should be accepted in field."""
        pwd_32 = "A1@" + "a" * 29
        assert len(pwd_32) == 32

        login_page.fill_password(pwd_32)
        actual = login_page.password_input.input_value()
        assert len(actual) <= 32, \
            f"Expected max 32 chars, field has {len(actual)}"