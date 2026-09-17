"""
Test: Password field hiển thị dạng masked (không hiển thị plain text)
Test Case: tc_003
Feature: User Login Form (feat_001)
Layer: ui | Coverage: happy
"""
import pytest
from pages.login_page import LoginPage


class TestPasswordMasked:
    """TC-003: Verify password field uses type='password' to mask input"""

    def test_password_field_is_masked(self, login_page: LoginPage):
        """Happy path — password input has type='password' attribute."""

        # Step 1-3: Navigate, type password, verify type attribute
        login_page.fill_password("TestPass123!")
        login_page.expect_password_masked()