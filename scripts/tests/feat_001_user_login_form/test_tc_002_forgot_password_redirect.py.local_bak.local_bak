"""
Test: Forgot Password link chuyển hướng đến trang khôi phục mật khẩu
Test Case: tc_002
Feature: User Login Form (feat_001)
Layer: ui | Coverage: happy
"""
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage


class TestForgotPasswordRedirect:
    """TC-002: Verify Forgot Password link redirects to recovery page"""

    def test_forgot_password_link_exists_and_redirects(self, login_page: LoginPage):
        """Forgot Password link must be present and clickable — spec requirement.

        FAIL if: link missing → BUG (spec requires it but no UI element).
        FAIL if: link present but click does nothing → BUG.
        """
        # Verify link exists — if not, this is a spec compliance bug
        link = login_page.forgot_password_link
        assert link.is_visible(), (
            "BUG: Forgot Password link không hiển thị trên login form. "
            "Spec yêu cầu 'Forgot Password link' nhưng không tìm thấy trên giao diện."
        )

        # Click and verify navigation — if still on same page, that's a bug
        link.click()
        assert "forgot" in login_page.page.url.lower() or \
               login_page.page.url != login_page.page.url, \
            "BUG: Click Forgot Password link không chuyển hướng đến trang khôi phục mật khẩu"