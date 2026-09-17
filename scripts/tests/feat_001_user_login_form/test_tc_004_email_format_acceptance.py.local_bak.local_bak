"""
Test: Email input field chấp nhận nhiều định dạng email hợp lệ
Test Case: tc_004
Feature: User Login Form (feat_001)
Layer: functional | Coverage: boundary

Runs against practice test site — field accepts input even if auth fails.
"""
import pytest
from pages.login_page import LoginPage
from helpers.data_generator import invalid_emails


VALID_EMAILS = [
    "user@example.com",
    "user+tag@example.com",
    "user@sub.example.com",
]


class TestEmailFormatAcceptance:
    """TC-004: Verify email field accepts all valid formats"""

    @pytest.mark.parametrize("email", VALID_EMAILS)
    def test_valid_email_accepted(self, login_page: LoginPage, email: str):
        """Each valid email format should be accepted by the input field."""

        # Steps 2-4: Enter each valid email format
        login_page.fill_username(email)

        # Verify: value is actually set
        actual = login_page.username_input.input_value()
        assert actual == email, f"Expected '{email}' but got '{actual}'"