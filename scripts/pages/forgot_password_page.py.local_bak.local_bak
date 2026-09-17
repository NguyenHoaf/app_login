"""
ForgotPasswordPage — Page Object Model for password recovery flow.

Placeholder: the current test site does not have a real forgot-password page.
Extend when the actual app provides one.
"""
from playwright.sync_api import Page, expect


class ForgotPasswordPage:
    """Password recovery page interaction layer."""

    def __init__(self, page: Page):
        self.page = page

    @property
    def email_input(self):
        return self.page.locator("#email")

    @property
    def reset_button(self):
        return self.page.locator("button[type='submit']:has-text('Reset')")

    def expect_forgot_password_page(self):
        """Assert we navigated to the password recovery page."""
        expect(self.page).to_have_url(contains="forgot", timeout=30_000)
        expect(self.email_input).to_be_visible()