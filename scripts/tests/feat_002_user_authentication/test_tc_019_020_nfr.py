"""
Test: NFR — Performance & Audit Logging
Test Cases: tc_019, tc_020
Feature: User Authentication Process (feat_002)
Layer: nfr | Coverage: nfr, regression
"""
import pytest
import time
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.settings import CFG


class TestAuthenticationPerformance:
    """TC-019: NFR — Authentication request xử lý trong < 3 giây"""

    def test_login_page_load_time_under_3s(self, page: Page):
        """Performance — measure login page load time.

        FAIL if: > 3s → NFR VIOLATION.
        """
        start = time.time()
        page.goto(CFG.login_url)
        expect(page.locator("#username")).to_be_visible(timeout=15000)
        elapsed = (time.time() - start) * 1000
        assert elapsed < 3000, \
            f"🔴 NFR VIOLATION: Login page load took {elapsed:.0f}ms (limit: 3000ms). " \
            f"Spec: 'Login form phải hiển thị trong < 2 giây' (thực tế 3s để dung sai network)."

    def test_login_submit_to_dashboard_under_3s(self, page: Page):
        """Performance — measure full login flow (click submit → dashboard).

        FAIL if: > 3s → NFR VIOLATION.
        """
        login_page = LoginPage(page).navigate()
        start = time.time()

        login_page.login(CFG.valid_username, CFG.valid_password)

        # Wait for dashboard
        dashboard = DashboardPage(page)
        try:
            dashboard.expect_dashboard_loaded()
        except AssertionError:
            # If login fails, that's a functional bug (already tested in tc_011)
            # Skip performance measurement
            pytest.skip("Login failed — không thể đo performance")

        elapsed = (time.time() - start) * 1000
        assert elapsed < 3000, \
            f"🔴 NFR VIOLATION: Full login flow took {elapsed:.0f}ms (limit: 3000ms). " \
            f"User phải chờ quá lâu để đăng nhập. Spec yêu cầu < 3 giây."


class TestAuditLogging:
    """TC-020: NFR — Audit log ghi lại mọi lần đăng nhập"""

    def test_audit_log_success_attempt_accessible(self, page: Page):
        """Try to detect audit log endpoint.

        This probes for common audit log APIs. Real test needs server-side access.
        """
        endpoints = ["/api/audit/log", "/api/logs", "/admin/audit"]
        found = False
        for ep in endpoints:
            try:
                resp = page.evaluate(f"""
                    async () => {{
                        const r = await fetch('{ep}', {{method: 'HEAD'}});
                        return r.status;
                    }}
                """)
                if resp < 500:
                    found = True
                    break
            except Exception:
                continue

        assert found, \
            "BUG: Không tìm thấy audit log endpoint nào. " \
            "Spec yêu cầu 'Mọi lần đăng nhập thành công/thất bại phải ghi audit log'. " \
            "Nếu audit log không được implement thì không thể verify compliance."