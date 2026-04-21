"""
Financial calculator logic.
Pure functions for financial calculations.
"""

from typing import Dict, Any


def calculate_percentage(amount: float, percentage: float) -> float:
    """Calculate percentage of an amount."""
    return (amount * percentage) / 100


def calculate_discount(price: float, discount_percent: float) -> Dict[str, float]:
    """Calculate discounted price and savings."""
    discount_amount = (price * discount_percent) / 100
    final_price = price - discount_amount
    return {
        "original_price": price,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "final_price": final_price,
        "savings": discount_amount
    }


def calculate_loan_payment(
    principal: float,
    annual_rate: float,
    years: int
) -> Dict[str, float]:
    """
    Calculate monthly loan payment using amortization formula.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (percentage)
        years: Loan term in years
    
    Returns:
        Dictionary with payment details
    """
    if annual_rate == 0:
        monthly_payment = principal / (years * 12)
    else:
        monthly_rate = (annual_rate / 100) / 12
        num_payments = years * 12
        monthly_payment = principal * (
            (monthly_rate * (1 + monthly_rate) ** num_payments) /
            ((1 + monthly_rate) ** num_payments - 1)
        )
    
    total_payment = monthly_payment * (years * 12)
    total_interest = total_payment - principal
    
    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "years": years,
        "monthly_payment": monthly_payment,
        "total_payment": total_payment,
        "total_interest": total_interest
    }


def calculate_roi(investment: float, return_value: float) -> Dict[str, float]:
    """
    Calculate Return on Investment (ROI).
    
    Args:
        investment: Initial investment amount
        return_value: Final return value
    
    Returns:
        Dictionary with ROI details
    """
    profit = return_value - investment
    roi_percent = (profit / investment) * 100 if investment != 0 else 0
    
    return {
        "investment": investment,
        "return_value": return_value,
        "profit": profit,
        "roi_percent": roi_percent
    }


def calculate_vat(amount: float, vat_rate: float, inclusive: bool = False) -> Dict[str, float]:
    """
    Calculate VAT (Value Added Tax).
    
    Args:
        amount: Amount to calculate VAT for
        vat_rate: VAT rate percentage
        inclusive: Whether the amount already includes VAT
    
    Returns:
        Dictionary with VAT details
    """
    if inclusive:
        vat_amount = amount - (amount / (1 + vat_rate / 100))
        net_amount = amount - vat_amount
    else:
        vat_amount = (amount * vat_rate) / 100
        net_amount = amount
    
    gross_amount = net_amount + vat_amount
    
    return {
        "net_amount": net_amount,
        "vat_rate": vat_rate,
        "vat_amount": vat_amount,
        "gross_amount": gross_amount,
        "inclusive": inclusive
    }


def compound_interest(
    principal: float,
    annual_rate: float,
    years: int,
    compounds_per_year: int = 12
) -> Dict[str, float]:
    """
    Calculate compound interest.
    
    Args:
        principal: Initial principal balance
        annual_rate: Annual interest rate (percentage)
        years: Number of years
        compounds_per_year: Number of times interest is compounded per year
    
    Returns:
        Dictionary with compound interest details
    """
    rate_decimal = annual_rate / 100
    amount = principal * (1 + rate_decimal / compounds_per_year) ** (compounds_per_year * years)
    interest_earned = amount - principal
    
    return {
        "principal": principal,
        "final_amount": amount,
        "interest_earned": interest_earned,
        "annual_rate": annual_rate,
        "years": years,
        "compounds_per_year": compounds_per_year
    }
