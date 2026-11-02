"""
Decimal and Monetary Utilities
Ensures exact financial calculations using Python's Decimal type,
preventing IEEE 754 floating point inaccuracies in healthcare billing.
"""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Union, Tuple


CENT = Decimal("0.01")


def to_decimal(value: Union[str, int, float, Decimal, None], default: str = "0.00") -> Decimal:
    """
    Safely converts input value into a 2-decimal-place Decimal object.
    Always uses quantize with ROUND_HALF_UP.
    """
    if value is None:
        value = default

    try:
        if isinstance(value, float):
            # Convert float via string representation to avoid precision leaks
            d = Decimal(str(value))
        else:
            d = Decimal(str(value).strip())
        return d.quantize(CENT, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"Cannot convert '{value}' to a valid monetary Decimal.") from exc


def calculate_balance(total_amount: Union[Decimal, str, float],
                      paid_amount: Union[Decimal, str, float]) -> Decimal:
    """Calculates balance_due = total_amount - paid_amount."""
    total = to_decimal(total_amount)
    paid = to_decimal(paid_amount)
    return (total - paid).quantize(CENT, rounding=ROUND_HALF_UP)


def validate_billing_math(total_amount: Union[Decimal, str, float],
                          paid_amount: Union[Decimal, str, float],
                          balance_due: Union[Decimal, str, float]) -> Tuple[bool, str]:
    """
    Validates monetary integrity:
    1. total_amount >= 0
    2. paid_amount >= 0
    3. balance_due >= 0
    4. paid_amount <= total_amount
    5. paid_amount + balance_due == total_amount
    """
    try:
        total = to_decimal(total_amount)
        paid = to_decimal(paid_amount)
        balance = to_decimal(balance_due)
    except ValueError as e:
        return False, str(e)

    if total < Decimal("0.00"):
        return False, f"Total amount cannot be negative: {total}"

    if paid < Decimal("0.00"):
        return False, f"Paid amount cannot be negative: {paid}"

    if balance < Decimal("0.00"):
        return False, f"Balance due cannot be negative: {balance}"

    if paid > total:
        return False, f"Paid amount ({paid}) cannot exceed total amount ({total})"

    if (paid + balance) != total:
        return False, f"Sum of paid ({paid}) and balance ({balance}) must equal total ({total})"

    return True, "Valid"


def format_currency(amount: Union[Decimal, str, float, None]) -> str:
    """Formats Decimal as USD string (e.g., $1,250.00)."""
    if amount is None:
        return "$0.00"
    dec = to_decimal(amount)
    return f"${dec:,.2f}"
