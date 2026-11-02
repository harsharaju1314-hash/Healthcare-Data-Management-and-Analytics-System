"""
Unit Tests for Decimal and Monetary Utility Functions
Verifies exact financial arithmetic without binary floating point drift.
"""

import pytest
from decimal import Decimal
from app.utils.decimal_utils import to_decimal, calculate_balance, validate_billing_math, format_currency


def test_exact_decimal_conversion():
    d = to_decimal("120.50")
    assert d == Decimal("120.50")
    assert str(d) == "120.50"


def test_no_float_precision_leak():
    # 0.1 + 0.2 in standard IEEE 754 float is 0.30000000000000004
    a = to_decimal(0.1)
    b = to_decimal(0.2)
    assert a + b == Decimal("0.30")


def test_calculate_balance():
    total = "250.00"
    paid = "100.00"
    bal = calculate_balance(total, paid)
    assert bal == Decimal("150.00")


def test_validate_billing_math_valid():
    is_valid, msg = validate_billing_math(Decimal("300.00"), Decimal("100.00"), Decimal("200.00"))
    assert is_valid is True
    assert msg == "Valid"


def test_validate_billing_math_invalid_sum():
    # 100 + 150 != 300
    is_valid, msg = validate_billing_math(Decimal("300.00"), Decimal("100.00"), Decimal("150.00"))
    assert is_valid is False
    assert "Sum of paid" in msg


def test_validate_billing_math_negative_total():
    is_valid, msg = validate_billing_math(Decimal("-50.00"), Decimal("0.00"), Decimal("-50.00"))
    assert is_valid is False
    assert "cannot be negative" in msg


def test_validate_billing_math_paid_exceeds_total():
    is_valid, msg = validate_billing_math(Decimal("100.00"), Decimal("150.00"), Decimal("-50.00"))
    assert is_valid is False
    assert "cannot be negative" in msg or "cannot exceed" in msg


def test_format_currency():
    assert format_currency("1250.75") == "$1,250.75"
    assert format_currency(0) == "$0.00"
    assert format_currency(None) == "$0.00"
