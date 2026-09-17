"""
Test data generators — produce boundary values, invalid formats, edge cases.

Avoids hardcoding magic strings across multiple test files.
"""
from config.settings import CFG


def long_email(length: int = None) -> str:
    """Generate an email that exceeds max length."""
    n = length or CFG.email_max_length + 1
    local_part = "a" * (n - len("@x.co"))
    return f"{local_part}@x.co"


def short_password(length: int = None) -> str:
    """Generate a password shorter than minimum length."""
    n = length or CFG.password_min_length - 1
    return "A" + "a" * max(0, n - 1)


def long_password(length: int = None) -> str:
    """Generate a password that exceeds maximum length."""
    n = length or CFG.password_max_length + 1
    return "A1@" + "a" * max(0, n - 3)


def nullish_values() -> list:
    """Return a list of values that should be treated as empty."""
    return ["", "  ", "\t", "\n", None]


def invalid_emails() -> list:
    """Return a list of invalid email formats for negative testing."""
    return [
        "notanemail",
        "user@",
        "@domain.com",
        "user@domain",
        "user@.com",
        "user name@domain.com",
        "user@domain..com",
        "",
        "  ",
    ]


def sql_injection_payloads() -> list:
    """Common SQL injection strings for security testing."""
    return [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users; --",
        "\" OR 1=1 --",
        "admin' --",
        "1; SELECT * FROM admin --",
    ]


def xss_payloads() -> list:
    """Common XSS strings for security testing."""
    return [
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert(1)>",
        "\"><script>alert(1)</script>",
        "javascript:alert(1)",
        "<svg/onload=alert(1)>",
    ]