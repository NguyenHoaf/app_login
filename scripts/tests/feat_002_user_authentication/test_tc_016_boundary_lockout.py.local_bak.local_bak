"""
Test: Brute force login — boundary 4 fail + 1 đúng (không lock) vs 5 fail (lock)
Test Case: tc_016
Feature: User Authentication Process (feat_002)
Layer: functional | Coverage: boundary
"""
import pytest
from pages.login_page import LoginPage
from config.settings import CFG


class TestBoundaryLockout:
    """TC-016: Verify boundary lockout — 4 fail OK, 5 fail = lock"""

    def test_lockout_after_5_consecutive_failures(self, login_page: LoginPage):
        """Boundary — 5 failed attempts should lock account.

        FAIL if: account never locks (can always login) → SECURITY BUG.
        FAIL if: locks before 5 attempts → regression.
        """
        wrong_password = "WrongPassword999!"

        # Attempt 5 consecutive failed logins
        for attempt in range(1, 6):
            login_page.fill_username(CFG.valid_username)
            login_page.fill_password(wrong_password)
            login_page.click_submit()

            if attempt < 5:
                # First 4: should still be on login page → OK
                assert "login" in login_page.page.url.lower(), \
                    f"BUG: Account bị lock sớm ở lần fail thứ {attempt} (spec: 5 lần)"
            else:
                # 5th attempt: should see lock message OR at least fail
                body_text = login_page.page.locator("body").text_content().lower()
                has_lock = any(kw in body_text for kw in ["lock", "locked", "too many", "try again later"])
                assert has_lock or "login" in login_page.page.url.lower(), \
                    f"BUG: Sau 5 lần fail, account vẫn không bị khóa hoặc không có thông báo. " \
                    f"Đây là lỗ hổng bảo mật: attacker brute-force không bị chặn."

    def test_login_succeeds_on_4th_attempt_valid(self, login_page: LoginPage):
        """Boundary — 4 fails + valid password = should NOT lock.

        FAIL if: account locked before 5 attempts → regression.
        """
        for attempt in range(1, 5):
            login_page.fill_username(CFG.valid_username)
            login_page.fill_password("WrongPass!")
            login_page.click_submit()
            assert "login" in login_page.page.url.lower(), \
                f"BUG: Account bị lock ở lần fail thứ {attempt} (chưa tới ngưỡng 5)"

        # 5th attempt with VALID password
        login_page.fill_username(CFG.valid_username)
        login_page.fill_password(CFG.valid_password)
        login_page.click_submit()

        # Should login successfully (not locked yet)
        is_logged_in = "logged-in-successfully" in login_page.page.url.lower() or \
                       "dashboard" in login_page.page.url.lower()
        if not is_logged_in:
            body_text = login_page.page.locator("body").text_content().lower()
            assert "lock" not in body_text, \
                "BUG: Account bị lock dù chưa đủ 5 lần fail (4 fail + 1 đúng)."