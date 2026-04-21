"""
Mathematical calculator logic.
Pure functions for basic and advanced mathematical operations.
"""

import math
from typing import Union


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b


def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    return math.pow(base, exponent)


def square_root(value: float) -> float:
    """Calculate square root of a number."""
    if value < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(value)


def logarithm(value: float, base: float = math.e) -> float:
    """Calculate logarithm of value with given base."""
    if value <= 0:
        raise ValueError("Logarithm undefined for non-positive values")
    if base <= 0 or base == 1:
        raise ValueError("Invalid logarithm base")
    return math.log(value, base)


def sine(angle: float, degrees: bool = False) -> float:
    """Calculate sine of an angle."""
    if degrees:
        angle = math.radians(angle)
    return math.sin(angle)


def cosine(angle: float, degrees: bool = False) -> float:
    """Calculate cosine of an angle."""
    if degrees:
        angle = math.radians(angle)
    return math.cos(angle)


def tangent(angle: float, degrees: bool = False) -> float:
    """Calculate tangent of an angle."""
    if degrees:
        angle = math.radians(angle)
    return math.tan(angle)


def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    return math.factorial(n)


def percentage(value: float, percent: float) -> float:
    """Calculate percentage of a value."""
    return (value * percent) / 100
