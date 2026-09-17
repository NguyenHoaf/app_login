"""
Test: Đăng nhập với email đúng nhưng sai password
Test Case: tc_013
Feature: User Authentication Process (feat_002)
Layer: e2e | Coverage: negative
"""
import pytest
from pages.login_page import LoginPage
from config.settings import CFG


class TestWrongPassword:
    """TC-013: Verify sai password → error message hiển thị"""

    def test_wrong_password_shows_error(self, login_page: LoginPage):
        """Negative — valid username, wrong password → 'Your password is invalid!'."""

        # Steps 1-3: Fill valid username + wrong password, submit
        login_page.login(CFG.valid_username, CFG.wrong_password)

        # Verify: error message
        login_page.expect_error_message("Your password is invalid!")
        login_page.expect_still_on_login_page()