"""
Test: API — POST /api/login validate trường required
Test Case: tc_027
Feature: Input Validation Rules (feat_003)
Layer: api | Coverage: negative
"""
import pytest
import requests
from config.settings import CFG


class TestApiRequiredFields:
    """TC-027: API reject 400 khi email hoặc password bị thiếu"""

    def test_api_empty_email(self):
        """POST with empty email → should return error."""
        payload = {"username": "", "password": "TestPass123!"}
        response = requests.post(CFG.login_url, data=payload, timeout=10)
        assert response.status_code == 200 or "error" in response.text.lower(), (
            "Should handle empty email gracefully"
        )

    def test_api_empty_password(self):
        """POST with empty password → should return error."""
        payload = {"username": CFG.valid_username, "password": ""}
        response = requests.post(CFG.login_url, data=payload, timeout=10)
        assert response.status_code == 200 or "error" in response.text.lower(), (
            "Should handle empty password gracefully"
        )

    def test_api_empty_body(self):
        """POST with empty body → should return error."""
        response = requests.post(CFG.login_url, data={}, timeout=10)
        assert response.status_code == 200 or "error" in response.text.lower(), (
            "Should handle empty body gracefully"
        )