"""
Centralized test configuration — single source of truth for all test environments.

Usage:
    from config.settings import CFG

    CFG.base_url       # https://practicetestautomation.com
    CFG.credentials     # {user: ..., pass: ...}

Override with environment variables:
    export BASE_URL=https://staging.example.com
    export TEST_USER=admin
    export TEST_PASS=admin123
    export HEADLESS=true
"""
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TestConfig:
    # ── Application ──
    base_url: str = os.getenv("BASE_URL", "https://practicetestautomation.com")
    login_path: str = "/practice-test-login/"
    logged_in_path: str = "/logged-in-successfully/"

    # ── Credentials ──
    valid_username: str = os.getenv("TEST_USER", "student")
    valid_password: str = os.getenv("TEST_PASS", "Password123")

    # ── Browser ──
    browser: str = os.getenv("BROWSER", "chromium")      # chromium | firefox | webkit
    headless: bool = os.getenv("HEADLESS", "false").lower() == "true"
    slowmo: int = int(os.getenv("SLOWMO", "200"))         # ms between actions
    viewport_width: int = 1280
    viewport_height: int = 720
    timeout_ms: int = int(os.getenv("TIMEOUT_MS", "30000"))

    # ── Boundary values ──
    password_min_length: int = 10
    password_max_length: int = 32
    email_max_length: int = 255
    lockout_max_failures: int = 5
    lockout_duration_minutes: int = 30
    session_timeout_minutes: int = 120
    otp_max_attempts: int = 5

    # ── Test data ──
    nonexistent_username: str = "nonexistent@unknown.com"
    wrong_password: str = "WrongPassword456!"
    locked_username: str = "lockedaccount@test.com"

    # ── Feature folders (auto maps) ──
    feature_map: dict = field(default_factory=lambda: {
        "feat_001": "feat_001_user_login_form",
        "feat_002": "feat_002_user_authentication",
        "feat_003": "feat_003_input_validation",
        "feat_004": "feat_004_security_controls",
        "feat_005": "feat_005_browser_compatibility",
    })

    @property
    def login_url(self) -> str:
        return f"{self.base_url}{self.login_path}"

    @property
    def logged_in_url(self) -> str:
        return f"{self.base_url}{self.logged_in_path}"

    @property
    def credentials(self) -> dict:
        return {
            "username": self.valid_username,
            "password": self.valid_password,
        }


# Singleton
CFG = TestConfig()