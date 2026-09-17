"""
Test: Hiển thị form đăng nhập với đầy đủ các thành phần
Test Case: tc_001
Feature: User Login Form (feat_001)
Layer: ui | Coverage: happy
"""
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage


class TestLoginFormLayout:
    """TC-001: Verify login form hiển thị đầy đủ email, password, Login button"""

    def test_login_form_elements_visible(self, login_page: LoginPage):
        """Happy path — form renders all expected elements on the practice site."""

        # Step 1-5: Verify form elements
        login_page.expect_form_visible()

        # Verify the form structure on the practice site
        expect(login_page.username_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()
        expect(login_page.submit_button).to_be_visible()