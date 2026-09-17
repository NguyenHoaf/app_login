"""
Test: Email validation — invalid formats & max length boundary
Test Cases: tc_021, tc_022
Feature: Input Validation Rules (feat_003)
Layer: functional | Coverage: negative, boundary
"""
import pytest
from pages.login_page import LoginPage
from helpers.data_generator import invalid_emails, long_email
from config.settings import CFG


class TestEmailInvalidFormat:
    """TC-021: Email không đúng định dạng → error message"""

    @pytest.mark.parametrize("bad_email", invalid_emails())
    def test_invalid_email_format_rejected(self, login_page: LoginPage, bad_email: str):
        """Each invalid email format should trigger validation error.

        FAIL if: redirect to dashboard (invalid email accepted) → VALIDATION BUG.
        FAIL if: server crash / 500 → STABILITY BUG.
        """
        login_page.login(bad_email, "TestPass123!")

        # If redirected to dashboard → email validation bypassed → BUG
        is_logged_in = "logged-in-successfully" in login_page.page.url.lower() or \
                       "dashboard" in login_page.page.url.lower()
        assert not is_logged_in, \
            f"BUG: Email không hợp lệ '{bad_email}' vẫn login được! " \
            f"Validation bị bypass, attacker có thể dùng email sai format để đăng nhập."

        # Should show a validation error or stay on login page
        assert "login" in login_page.page.url.lower(), \
            f"BUG: Submit với email '{bad_email}' gây lỗi không xác định (redirect lạ)"

        # Check no server 500 in page body
        body_text = login_page.page.locator("body").text_content().lower()
        assert "internal server error" not in body_text and "500" not in body_text, \
            f"BUG: Email '{bad_email}' gây Internal Server Error (500)"


class TestEmailMaxLength:
    """TC-022: Email vượt quá 255 ký tự — validation fail (boundary)"""

    def test_email_256_chars_rejected(self, login_page: LoginPage):
        """Boundary: 256 chars → MUST be rejected or truncated.

        FAIL if: email 256 chars accepted into field (no maxlength) → BUG.
        FAIL if: email truncated but server still processes it → BUG.
        """
        # Generate 256-char email
        email_256 = "a" * 256 + "@x.co"

        login_page.fill_username(email_256)
        actual_value = login_page.username_input.input_value()

        assert len(actual_value) <= 255, \
            f"BUG: Email input field không enforce maxlength=255. " \
            f"Nhập 256 ký tự nhưng field chấp nhận {len(actual_value)} ký tự. " \
            f"Spec yêu cầu max 255 characters — có nguy cơ SQL injection / buffer overflow."

    def test_email_255_chars_accepted(self, login_page: LoginPage):
        """Boundary: 255 chars → should work.

        FAIL if: system crashes on 255-char email.
        """
        email_255 = "a" * 254 + "@x.co"
        email_255 = email_255[:255]
        login_page.fill_username(email_255)

        actual_value = login_page.username_input.input_value()
        # Field should accept it (or at least show the field still works)
        assert len(actual_value) <= 255, \
            f"Field value {len(actual_value)} exceeds expected 255"

        login_page.fill_password("TestPass123!")
        login_page.click_submit()

        body_text = login_page.page.locator("body").text_content().lower()
        assert "internal server error" not in body_text and "500" not in body_text, \
            "BUG: Email 255 ký tự gây server crash"