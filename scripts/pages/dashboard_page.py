"""
DashboardPage — Page Object Model for the post-login dashboard.

Verifies successful login indicators and provides dashboard-level actions.
"""
from playwright.sync_api import Page, expect
from config.settings import CFG


class DashboardPage:
    """Dashboard / logged-in-successfully page interaction layer."""

    def __init__(self, page: Page):
        self.page = page

    # ── Locators ──────────────────────────────────────────────────────────
    @property
    def heading(self):
        return self.page.locator("h1")

    @property
    def body(self):
        return self.page.locator("body")

    @property
    def logout_link(self):
        return self.page.get_by_role("link", name="Log out")

    @property
    def congratulations_msg(self):
        return self.page.locator("text=Congratulations")

    @property
    def success_msg(self):
        return self.page.locator("text=successfully logged in")

    # ── Actions ───────────────────────────────────────────────────────────

    def expect_dashboard_loaded(self):
        """Assert we are on the logged-in success page with all indicators."""
        expect(self.page).to_have_url(CFG.logged_in_url, timeout=CFG.timeout_ms)
        expect(self.heading).to_contain_text("Logged In Successfully")
        expect(self.congratulations_msg).to_be_visible()
        expect(self.success_msg).to_be_visible()
        expect(self.logout_link).to_be_visible()

    def click_logout(self) -> "DashboardPage":
        """Log out and return to login page."""
        self.logout_link.click()
        expect(self.page).to_have_url(CFG.login_url, timeout=CFG.timeout_ms)
        return self