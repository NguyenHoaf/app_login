"""
LoginPage — Page Object Model for the login form.

Locators and actions centralised so selector changes only affect this file.
"""
from playwright.sync_api import Page, expect
from config.settings import CFG


class LoginPage:
    """Login form interaction layer."""

    def __init__(self, page: Page):
        self.page = page

    # ── Locators ──────────────────────────────────────────────────────────
    @property
    def username_input(self):
        return self.page.locator("#username")

    @property
    def password_input(self):
        return self.page.locator("#password")

    @property
    def submit_button(self):
        return self.page.locator("#submit")

    @property
    def error_message(self):
        return self.page.locator("#error")

    @property
    def forgot_password_link(self):
        return self.page.locator("a:has-text('Forgot Password')")

    @property
    def login_form(self):
        return self.page.locator("form")

    # ── Actions ───────────────────────────────────────────────────────────

    def navigate(self) -> "LoginPage":
        """Go to the login page and wait for form to be ready."""
        self.page.goto(CFG.login_url)
        self.expect_form_visible()
        return self

    def expect_form_visible(self):
        """Assert the login form elements are rendered."""
        expect(self.username_input).to_be_visible(timeout=CFG.timeout_ms)
        expect(self.password_input).to_be_visible(timeout=CFG.timeout_ms)
        expect(self.submit_button).to_be_visible(timeout=CFG.timeout_ms)

    def fill_username(self, username: str) -> "LoginPage":
        """Type into the username field."""
        self.username_input.fill(username)
        return self

    def fill_password(self, password: str) -> "LoginPage":
        """Type into the password field."""
        self.password_input.fill(password)
        return self

    def fill_credentials(self, username: str, password: str) -> "LoginPage":
        """Fill both fields in one call (fluent)."""
        self.fill_username(username)
        self.fill_password(password)
        return self

    def click_submit(self) -> "LoginPage":
        """Click the Submit / Login button."""
        self.submit_button.click()
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Convenience: fill + submit in one call."""
        self.fill_credentials(username, password)
        self.click_submit()
        return self

    def click_forgot_password(self) -> "LoginPage":
        """Click the Forgot Password link."""
        self.forgot_password_link.click()
        return self

    # ── Assertions ────────────────────────────────────────────────────────

    def expect_error_message(self, expected_text: str):
        """Assert a specific error message is displayed."""
        expect(self.error_message).to_be_visible(timeout=CFG.timeout_ms)
        expect(self.error_message).to_contain_text(expected_text)

    def expect_still_on_login_page(self):
        """Assert the URL is still the login page (no redirect)."""
        expect(self.page).to_have_url(CFG.login_url)

    def expect_password_masked(self):
        """Assert the password field has type='password' (masked)."""
        input_type = self.password_input.get_attribute("type")
        assert input_type == "password", f"Expected type=password, got {input_type}"

    def expect_username_placeholder(self, placeholder: str = ""):
        """Assert placeholder text on username field (if defined in spec)."""
        if placeholder:
            expect(self.username_input).to_have_attribute("placeholder", placeholder)

    def expect_password_placeholder(self, placeholder: str = ""):
        """Assert placeholder text on password field (if defined in spec)."""
        if placeholder:
            expect(self.password_input).to_have_attribute("placeholder", placeholder)