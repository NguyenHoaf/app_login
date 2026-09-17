"""
Test: Đăng nhập với email không tồn tại trong hệ thống
Test Case: tc_012
Feature: User Authentication Process (feat_002)
Layer: e2e | Coverage: negative
"""
import pytest
from pages.login_page import LoginPage
from config.settings import CFG


class TestLoginInvalidUsername:
    """TC-012: Verify user nhập username không tồn tại → error message hiển thị"""

    def test_login_nonexistent_username(self, login_page: LoginPage):
        """Negative — nonexistent username → error, no redirect."""

        # Step 1-3: Navigate, fill invalid credentials, submit
        login_page.login(CFG.nonexistent_username, "TestPass123!")

        # Verify: error message "Your username is invalid!"
        login_page.expect_error_message("Your username is invalid!")

        # Verify: still on login page (no redirect)
        login_page.expect_still_on_login_page()