"""
Test: Đăng nhập khi account bị locked
Test Case: tc_014
Feature: User Authentication Process (feat_002)
Layer: e2e | Coverage: negative
"""
import pytest
from pages.login_page import LoginPage
from config.settings import CFG


class TestLockedAccount:
    """TC-014: Verify locked account cannot log in"""

    def test_locked_account_gets_lock_message(self, login_page: LoginPage):
        """Negative — locked account → 'Your account has been locked.'

        Spec: Account locked after 5 failed attempts.
        FAIL if: login succeeds (lock not implemented) → SECURITY BUG.
        FAIL if: wrong error message → BUG.
        """
        # Attempt to login with locked account credentials
        login_page.login(CFG.locked_username, "anypassword")

        # If redirected to dashboard → account lock NOT enforced → SECURITY BUG
        assert "login" in login_page.page.url.lower() or \
               "error" in login_page.page.url.lower(), \
            "BUG: Account locking không được enforce — login vẫn thành công dù account bị lock. " \
            "Đây là lỗ hổng bảo mật: attacker có thể brute-force dù account đã bị lock."

        # Check for lock message (or any error — site may show different message)
        body_text = login_page.page.locator("body").text_content()
        has_lock_message = any(kw in body_text.lower() for kw in ["lock", "locked", "suspend", "block"])
        assert has_lock_message, \
            f"BUG: Account locked nhưng không hiển thị lock message. " \
            f"Body content: {body_text[:200]}..."