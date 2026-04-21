"""
API routes for calculator endpoints.
Handles HTTP requests and responses, delegates to calculator logic.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from app.calculators import math_ops, finance_ops, health_ops, converter_ops


router = APIRouter(prefix="/api", tags=["calculators"])


# ==================== Math Calculator Schemas ====================

class MathOperation(BaseModel):
    operation: str = Field(..., description="Operation type")
    a: Optional[float] = None
    b: Optional[float] = None
    value: Optional[float] = None
    base: Optional[float] = None
    exponent: Optional[float] = None
    angle: Optional[float] = None
    degrees: bool = False
    n: Optional[int] = None
    percent: Optional[float] = None


# ==================== Finance Calculator Schemas ====================

class DiscountRequest(BaseModel):
    price: float = Field(..., gt=0)
    discount_percent: float = Field(..., ge=0, le=100)


class LoanRequest(BaseModel):
    principal: float = Field(..., gt=0)
    annual_rate: float = Field(..., ge=0)
    years: int = Field(..., gt=0)


class ROIRequest(BaseModel):
    investment: float = Field(..., gt=0)
    return_value: float = Field(..., ge=0)


class VATRequest(BaseModel):
    amount: float = Field(..., gt=0)
    vat_rate: float = Field(..., ge=0, le=100)
    inclusive: bool = False


class CompoundInterestRequest(BaseModel):
    principal: float = Field(..., gt=0)
    annual_rate: float = Field(..., ge=0)
    years: int = Field(..., gt=0)
    compounds_per_year: int = Field(default=12, gt=0)


# ==================== Health Calculator Schemas ====================

class BMIRequest(BaseModel):
    weight_kg: float = Field(..., gt=0)
    height_cm: float = Field(..., gt=0)


class BMRRequest(BaseModel):
    weight_kg: float = Field(..., gt=0)
    height_cm: float = Field(..., gt=0)
    age: int = Field(..., gt=0)
    gender: str = Field(..., pattern="^(male|female)$")


class WaterIntakeRequest(BaseModel):
    weight_kg: float = Field(..., gt=0)
    activity_minutes: int = Field(default=0, ge=0)
    climate: str = Field(default="normal", pattern="^(normal|hot|cold)$")


class TDEERequest(BaseModel):
    weight_kg: float = Field(..., gt=0)
    height_cm: float = Field(..., gt=0)
    age: int = Field(..., gt=0)
    gender: str = Field(..., pattern="^(male|female)$")
    activity_level: str = Field(
        ..., 
        pattern="^(sedentary|lightly_active|moderately_active|very_active|extra_active)$"
    )


# ==================== Converter Schemas ====================

class ConvertRequest(BaseModel):
    value: float = Field(..., description="Value to convert")
    category: str = Field(..., pattern="^(length|weight|temperature|speed|data)$")
    from_unit: str = Field(..., description="Source unit")
    to_unit: str = Field(..., description="Target unit")


# ==================== Math Routes ====================

@router.post("/math/calculate")
def calculate_math(operation: MathOperation) -> Dict[str, Any]:
    """Perform mathematical calculations."""
    try:
        op = operation.operation
        
        if op == "add":
            result = math_ops.add(operation.a, operation.b)
        elif op == "subtract":
            result = math_ops.subtract(operation.a, operation.b)
        elif op == "multiply":
            result = math_ops.multiply(operation.a, operation.b)
        elif op == "divide":
            result = math_ops.divide(operation.a, operation.b)
        elif op == "power":
            result = math_ops.power(operation.base, operation.exponent)
        elif op == "sqrt":
            result = math_ops.square_root(operation.value)
        elif op == "log":
            result = math_ops.logarithm(operation.value, operation.base or 2.718281828)
        elif op == "sin":
            result = math_ops.sine(operation.angle, operation.degrees)
        elif op == "cos":
            result = math_ops.cosine(operation.angle, operation.degrees)
        elif op == "tan":
            result = math_ops.tangent(operation.angle, operation.degrees)
        elif op == "factorial":
            result = math_ops.factorial(operation.n)
        elif op == "percentage":
            result = math_ops.percentage(operation.value, operation.percent)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown operation: {op}")
        
        return {"success": True, "result": result, "operation": op}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Finance Routes ====================

@router.post("/finance/discount")
def calculate_discount(request: DiscountRequest) -> Dict[str, Any]:
    """Calculate discounted price."""
    result = finance_ops.calculate_discount(request.price, request.discount_percent)
    return {"success": True, **result}


@router.post("/finance/loan")
def calculate_loan(request: LoanRequest) -> Dict[str, Any]:
    """Calculate loan payment details."""
    result = finance_ops.calculate_loan_payment(
        request.principal, request.annual_rate, request.years
    )
    return {"success": True, **result}


@router.post("/finance/roi")
def calculate_roi(request: ROIRequest) -> Dict[str, Any]:
    """Calculate Return on Investment."""
    result = finance_ops.calculate_roi(request.investment, request.return_value)
    return {"success": True, **result}


@router.post("/finance/vat")
def calculate_vat(request: VATRequest) -> Dict[str, Any]:
    """Calculate VAT."""
    result = finance_ops.calculate_vat(request.amount, request.vat_rate, request.inclusive)
    return {"success": True, **result}


@router.post("/finance/compound-interest")
def calculate_compound_interest(request: CompoundInterestRequest) -> Dict[str, Any]:
    """Calculate compound interest."""
    result = finance_ops.compound_interest(
        request.principal,
        request.annual_rate,
        request.years,
        request.compounds_per_year
    )
    return {"success": True, **result}


# ==================== Health Routes ====================

@router.post("/health/bmi")
def calculate_bmi(request: BMIRequest) -> Dict[str, Any]:
    """Calculate Body Mass Index."""
    result = health_ops.calculate_bmi(request.weight_kg, request.height_cm)
    return {"success": True, **result}


@router.post("/health/bmr")
def calculate_bmr(request: BMRRequest) -> Dict[str, Any]:
    """Calculate Basal Metabolic Rate."""
    result = health_ops.calculate_bmr(
        request.weight_kg, request.height_cm, request.age, request.gender
    )
    return {"success": True, **result}


@router.post("/health/water-intake")
def calculate_water_intake(request: WaterIntakeRequest) -> Dict[str, Any]:
    """Calculate daily water intake recommendation."""
    result = health_ops.calculate_daily_water_intake(
        request.weight_kg, request.activity_minutes, request.climate
    )
    return {"success": True, **result}


@router.post("/health/tdee")
def calculate_tdee(request: TDEERequest) -> Dict[str, Any]:
    """Calculate Total Daily Energy Expenditure."""
    result = health_ops.calculate_tdee(
        request.weight_kg,
        request.height_cm,
        request.age,
        request.gender,
        request.activity_level
    )
    return {"success": True, **result}


# ==================== Converter Routes ====================

@router.post("/converter/convert")
def convert_units(request: ConvertRequest) -> Dict[str, Any]:
    """Convert between units."""
    try:
        result = converter_ops.convert(
            request.value,
            request.category,
            request.from_unit,
            request.to_unit
        )
        return {"success": True, **result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/converter/units/{category}")
def get_units(category: str) -> Dict[str, Any]:
    """Get available units for a category."""
    try:
        units = converter_ops.get_available_units(category)
        return {"success": True, "category": category, "units": units}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/converter/categories")
def get_categories() -> Dict[str, Any]:
    """Get all available converter categories."""
    return {
        "success": True,
        "categories": ["length", "weight", "temperature", "speed", "data"]
    }
