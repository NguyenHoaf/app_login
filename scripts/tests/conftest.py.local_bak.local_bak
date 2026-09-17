"""
Pytest conftest — shared fixtures for Playwright test automation.

Provides fixture-based Playwright page instance + POM page objects following
industrial standards (https://playwright.dev/python/docs/test-runners).

Usage:
    def test_login(login_page: LoginPage):       # Auto-navigates to /login
    def test_dashboard(page: Page, dashboard_page: DashboardPage):
"""
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.forgot_password_page import ForgotPasswordPage
from config.settings import CFG


# ── Base Playwright fixtures (from pytest-playwright) ──────────────────────

@pytest.fixture(scope="function")
def page(context: Page) -> Page:
    """Provide a new browser page for each test function.

    Uses Playwright's built-in browser context fixture from
    pytest-playwright. Each test gets a clean page with isolated
    storage state.
    """
    new_page = context.new_page()
    new_page.set_viewport_size({"width": CFG.viewport_width, "height": CFG.viewport_height})
    yield new_page
    new_page.close()


# ── Page Object fixtures ──────────────────────────────────────────────────

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """LoginPage fixture — navigate to /login and return the page object."""
    return LoginPage(page).navigate()


@pytest.fixture
def dashboard_page(page: Page) -> DashboardPage:
    """DashboardPage fixture — does NOT navigate (use after login)."""
    return DashboardPage(page)


@pytest.fixture
def forgot_password_page(page: Page) -> ForgotPasswordPage:
    """ForgotPasswordPage fixture."""
    return ForgotPasswordPage(page)


# ── Authenticated session fixture ─────────────────────────────────────────

@pytest.fixture
def logged_in_session(login_page: LoginPage, dashboard_page: DashboardPage):
    """Log in once, yield (login_page, dashboard_page) tuple for reuse."""
    login_page.login(CFG.valid_username, CFG.valid_password)
    dashboard_page.expect_dashboard_loaded()
    yield login_page, dashboard_page


# ── Error / boundary data fixtures ────────────────────────────────────────

@pytest.fixture(params=[
    {"username": CFG.nonexistent_username, "password": "TestPass123!",
     "expected_error": "Your username is invalid!"},
])
def invalid_username_credentials(request):
    """Credentials where the username does not exist."""
    return request.param


@pytest.fixture(params=[
    {"username": CFG.valid_username, "password": CFG.wrong_password,
     "expected_error": "Your password is invalid!"},
])
def wrong_password_credentials(request):
    """Credentials where the username is valid but password is wrong."""
    return request.param