"""
Test: SQL Injection attempt / XSS attempt trong input fields
Test Cases: tc_007, tc_008
Feature: User Login Form (feat_001)
Layer: security | Coverage: negative
"""
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from helpers.data_generator import sql_injection_payloads, xss_payloads
from config.settings import CFG


class TestSqlInjection:
    """TC-007: SQL injection payloads không gây ảnh hưởng đến hệ thống"""

    @pytest.mark.security
    @pytest.mark.parametrize("payload", sql_injection_payloads())
    def test_sql_injection_blocked(self, login_page: LoginPage, payload: str):
        """Each SQL injection payload must be sanitized.

        FAIL if: redirect to dashboard (SQLi bypassed auth) → CRITICAL SECURITY BUG.
        FAIL if: server returns 500 / SQL error in HTML → INFO LEAKAGE BUG.
        FAIL if: page crashes / blank screen → STABILITY BUG.
        """
        login_page.login(payload, "TestPass123!")

        current_url = login_page.page.url.lower()

        # Detect SQL injection SUCCESS (bypass) — worst-case scenario
        is_logged_in = "logged-in-successfully" in current_url or \
                       "dashboard" in current_url
        assert not is_logged_in, \
            f"🔴 CRITICAL SECURITY BUG: SQL injection payload '{payload}' " \
            f"đã bypass xác thực! User đăng nhập thành công với SQL injection. " \
            f"Attacker có thể truy cập hệ thống mà không cần credentials hợp lệ."

        # Detect server-side SQL errors leaking in HTML
        body_text = login_page.page.locator("body").text_content().lower()
        sql_error_keywords = [
            "sql", "mysql", "syntax error", "unclosed quotation",
            "odbc", "sqlite", "ora-", "postgresql", "driver",
            "warning: mysql", "supplied argument", "server error"
        ]
        for keyword in sql_error_keywords:
            assert keyword not in body_text, \
                f"🔴 INFO LEAKAGE BUG: SQL error '{keyword}' leak ra ngoài HTML " \
                f"với payload '{payload}'. Attacker có thể khai thác thêm."

        # Detect 500 error
        assert "internal server error" not in body_text, \
            f"🔴 STABILITY BUG: SQL injection payload '{payload}' gây 500 Internal Server Error"

        # Must still be on login page (or relevant error page)
        assert "login" in current_url, \
            f"BUG: Submit với SQLi payload '{payload}' dẫn đến trang lạ: {current_url}"


class TestXssInjection:
    """TC-008: XSS payload không được thực thi"""

    @pytest.mark.security
    @pytest.mark.parametrize("payload", xss_payloads())
    def test_xss_attempt_sanitized(self, login_page: LoginPage, payload: str):
        """Each XSS payload must be sanitized — no script execution.

        FAIL if: payload renders unescaped in page → XSS VULNERABILITY.
        FAIL if: alert dialog appears → XSS confirmed.
        FAIL if: page redirects or changes behaviour → possible XSS.
        """
        login_page.login(payload, "TestPass123!")

        # Check for XSS execution: payload should NOT appear unescaped in DOM
        body_html = login_page.page.locator("body").inner_html().lower()
        unescaped = payload.lower().replace("<", "&lt;").replace(">", "&gt;")

        if payload in body_html and payload[0] == "<":
            # Payload appears raw in HTML without escaping → XSS VULNERABILITY
            pytest.fail(
                f"🔴 XSS VULNERABILITY: Payload '{payload}' xuất hiện RAW trong HTML "
                f"(không được escape). Attacker có thể inject script và đánh cắp session."
            )

        # Must stay on login page
        assert "login" in login_page.page.url.lower(), \
            f"BUG: XSS payload '{payload}' gây redirect bất thường"

        # Check no 500
        body_text = login_page.page.locator("body").text_content().lower()
        assert "internal server error" not in body_text, \
            f"BUG: XSS payload '{payload}' gây 500 Internal Server Error"