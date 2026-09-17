"""
Test: Security — HTTPS required, Session timeout, SQL injection, XSS
Test Cases: feat_004 ac_001-009 (no standalone TC numbers)
Feature: Security & Authentication Controls (feat_004)
Layer: security
"""
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from helpers.data_generator import sql_injection_payloads, xss_payloads
from config.settings import CFG


class TestHttpsRequired:
    """AC-001: Tất cả login requests phải qua HTTPS"""

    def test_login_page_uses_https(self, login_page: LoginPage):
        """Verify login page is served over HTTPS.

        FAIL if: HTTP (plain text) → CRITICAL SECURITY BUG (password in clear).
        """
        url = login_page.page.url
        assert url.startswith("https://"), \
            f"🔴 CRITICAL SECURITY BUG: Login page served over HTTP! " \
            f"URL: {url}. Password và credentials được gửi dưới dạng plain text. " \
            f"Spec yêu cầu HTTPS cho mọi login requests."


class TestSessionTimeout:
    """AC-003: Session timeout sau 2 giờ inactivity"""

    def test_session_does_not_expire_immediately(self, login_page: LoginPage):
        """Verify session lasts at least a few seconds (smoke).

        Note: Full 2h timeout requires long-running test.
        This smoke test verifies session doesn't expire instantly.
        """
        from pages.dashboard_page import DashboardPage
        login_page.login(CFG.valid_username, CFG.valid_password)
        dashboard = DashboardPage(login_page.page)
        dashboard.expect_dashboard_loaded()

        # Verify logout link works (session exists)
        expect(dashboard.logout_link).to_be_visible()
        dashboard.click_logout()


class TestSqlInjection:
    """AC-004: SQL injection attempt bị chặn"""

    @pytest.mark.parametrize("payload", sql_injection_payloads())
    def test_sql_injection_blocked(self, login_page: LoginPage, payload: str):
        """Each SQL injection payload must be sanitized.

        FAIL if: bypass auth (login success) → CRITICAL SECURITY BUG.
        FAIL if: SQL error leaks in HTML → INFO LEAKAGE.
        """
        login_page.login(payload, "TestPass123!")

        is_logged_in = "logged-in-successfully" in login_page.page.url.lower()
        assert not is_logged_in, \
            f"🔴 CRITICAL SECURITY BUG: SQLi '{payload}' bypass xác thực! " \
            f"Attacker login thành công với SQL injection."

        body_text = login_page.page.locator("body").text_content().lower()
        sql_errors = ["sql", "syntax error", "mysql", "ora-", "driver", "unclosed"]
        for err in sql_errors:
            assert err not in body_text, \
                f"🔴 INFO LEAKAGE: SQL error '{err}' xuất hiện trong HTML " \
                f"với payload '{payload}'. Database structure bị leak."

        assert "login" in login_page.page.url.lower(), \
            f"BUG: SQLi payload '{payload}' redirect lạ"


class TestXssBlocked:
    """AC-005: XSS attempt trong input fields bị sanitized"""

    @pytest.mark.parametrize("payload", xss_payloads())
    def test_xss_sanitized(self, login_page: LoginPage, payload: str):
        """Each XSS payload must be sanitized.

        FAIL if: payload renders raw in HTML → XSS VULNERABILITY.
        """
        login_page.login(payload, "TestPass123!")

        body_html = login_page.page.locator("body").inner_html().lower()
        if payload[0] == "<" and payload.lower() in body_html:
            unescaped = payload.lower().replace("&lt;", "<").replace("&gt;", ">")
            if unescaped == payload.lower():
                pytest.fail(
                    f"🔴 XSS VULNERABILITY: Payload '{payload}' xuất hiện raw trong HTML!"
                )

        assert "login" in login_page.page.url.lower(), \
            f"BUG: XSS payload '{payload}' gây redirect lạ"

        body_text = login_page.page.locator("body").text_content().lower()
        assert "internal server error" not in body_text, \
            f"BUG: XSS payload '{payload}' gây 500"


class TestTwoFactorAuth:
    """AC-006/007: 2FA setup & login flow"""

    def test_2fa_settings_page_not_found(self, login_page: LoginPage):
        """Try accessing /settings/2fa to check if 2FA endpoint exists.

        FAIL: trivially — documents that 2FA is not implemented.
        This test will fail on practice site, letting us know when 2FA is added.
        """
        login_page.page.goto(f"{CFG.base_url}/settings/2fa")
        status = login_page.page.evaluate("() => document.title || ''")
        assert "2fa" in status.lower() or "two-factor" in status.lower(), \
            "BUG: 2FA settings page không tồn tại hoặc không truy cập được. " \
            "Spec yêu cầu hỗ trợ 2FA (SMS + Authenticator App)."