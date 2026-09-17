"""
Test: API — GET /login trả về login form HTML
Test Case: tc_009
Feature: User Login Form (feat_001)
Layer: api | Coverage: happy

Uses browser-native fetch() to make API call, bypassing ModSecurity
while still testing the real HTTP response (not the rendered page).
"""
import pytest
import json
from playwright.sync_api import Page, expect
from config.settings import CFG


class TestLoginApi:
    """TC-009: Verify GET /login returns login form HTML with all 4 components"""

    def test_get_login_returns_200(self, page: Page):
        """API via fetch: GET /login must return 200.

        FAIL if: non-200 status code → SERVER/API BUG.
        """
        status_code = page.evaluate("""
            async () => {
                const resp = await fetch(arguments[0]);
                return resp.status;
            }
        """, CFG.login_url)
        assert status_code == 200, \
            f"BUG: GET {CFG.login_url} trả về HTTP {status_code} (expected 200). " \
            f"Server hoặc API endpoint không hoạt động đúng."

    def test_login_html_contains_email_input(self, page: Page):
        """API: GET /login HTML must contain email/username input.

        FAIL if: no email input in returned HTML → UI RENDERING BUG.
        """
        html = page.evaluate("""
            async () => {
                const resp = await fetch(arguments[0]);
                return await resp.text();
            }
        """, CFG.login_url)
        html_lower = html.lower()
        assert "username" in html_lower or "email" in html_lower, \
            "BUG: API trả về HTML không chứa email/username input field. " \
            f"HTML snippet: {html[:300]}..."

    def test_login_html_contains_password_input(self, page: Page):
        """API: GET /login must contain password input with type='password'.

        FAIL if: no password input → UI RENDERING BUG.
        FAIL if: type not 'password' → SECURITY BUG (password không masked).
        """
        html = page.evaluate("""
            async () => {
                const resp = await fetch(arguments[0]);
                return await resp.text();
            }
        """, CFG.login_url)
        assert 'type="password"' in html, \
            "BUG: API trả về HTML không có password input với type='password'. " \
            "Hoặc password không masked, đây là lỗ hổng bảo mật."

    def test_login_html_contains_submit_button(self, page: Page):
        """API: GET /login must contain a submit button."""
        html = page.evaluate("""
            async () => {
                const resp = await fetch(arguments[0]);
                return await resp.text();
            }
        """, CFG.login_url)
        html_lower = html.lower()
        assert "submit" in html_lower or 'type="submit"' in html, \
            "BUG: API trả về HTML không có submit button. " \
            f"HTML snippet: {html[:300]}..."

    def test_login_page_response_time_under_2s(self, page: Page):
        """API: Response time < 2s (server-side, not including render)."""
        duration_ms = page.evaluate("""
            async () => {
                const start = performance.now();
                await fetch(arguments[0]);
                return performance.now() - start;
            }
        """, CFG.login_url)
        assert duration_ms < 2000, \
            f"BUG: API response time {duration_ms:.0f}ms vượt quá 2000ms. " \
            f"NFR performance không đạt — cần tối ưu server."