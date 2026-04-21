"""
Unit converter logic.
Pure functions for converting between different units of measurement.
"""

from typing import Dict, Any, List


# Conversion rates to base units
LENGTH_UNITS = {
    "meter": 1.0,
    "kilometer": 1000.0,
    "centimeter": 0.01,
    "millimeter": 0.001,
    "mile": 1609.344,
    "yard": 0.9144,
    "foot": 0.3048,
    "inch": 0.0254,
    "nautical_mile": 1852.0
}

WEIGHT_UNITS = {
    "kilogram": 1.0,
    "gram": 0.001,
    "milligram": 0.000001,
    "metric_ton": 1000.0,
    "pound": 0.45359237,
    "ounce": 0.028349523125,
    "stone": 6.35029318,
    "us_ton": 907.18474,
    "imperial_ton": 1016.0469088
}

TEMPERATURE_UNITS = ["celsius", "fahrenheit", "kelvin"]

SPEED_UNITS = {
    "meter_per_second": 1.0,
    "kilometer_per_hour": 0.277777778,
    "mile_per_hour": 0.44704,
    "knot": 0.514444444,
    "foot_per_second": 0.3048
}

DATA_UNITS = {
    "byte": 1.0,
    "kilobyte": 1024.0,
    "megabyte": 1024.0 ** 2,
    "gigabyte": 1024.0 ** 3,
    "terabyte": 1024.0 ** 4,
    "petabyte": 1024.0 ** 5,
    "bit": 0.125,
    "kilobit": 1024.0 * 0.125,
    "megabit": (1024.0 ** 2) * 0.125,
    "gigabit": (1024.0 ** 3) * 0.125,
    "terabit": (1024.0 ** 4) * 0.125
}


def convert_length(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Convert length between units."""
    if from_unit not in LENGTH_UNITS or to_unit not in LENGTH_UNITS:
        raise ValueError("Invalid length unit")
    
    # Convert to meters first, then to target unit
    meters = value * LENGTH_UNITS[from_unit]
    result = meters / LENGTH_UNITS[to_unit]
    
    return {
        "input_value": value,
        "input_unit": from_unit,
        "output_value": round(result, 6),
        "output_unit": to_unit,
        "category": "length"
    }


def convert_weight(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Convert weight between units."""
    if from_unit not in WEIGHT_UNITS or to_unit not in WEIGHT_UNITS:
        raise ValueError("Invalid weight unit")
    
    # Convert to kilograms first, then to target unit
    kilograms = value * WEIGHT_UNITS[from_unit]
    result = kilograms / WEIGHT_UNITS[to_unit]
    
    return {
        "input_value": value,
        "input_unit": from_unit,
        "output_value": round(result, 6),
        "output_unit": to_unit,
        "category": "weight"
    }


def convert_temperature(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    if from_unit not in TEMPERATURE_UNITS or to_unit not in TEMPERATURE_UNITS:
        raise ValueError("Invalid temperature unit")
    
    # Convert to Celsius first
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = (value - 32) * 5/9
    else:  # kelvin
        celsius = value - 273.15
    
    # Convert from Celsius to target unit
    if to_unit == "celsius":
        result = celsius
    elif to_unit == "fahrenheit":
        result = celsius * 9/5 + 32
    else:  # kelvin
        result = celsius + 273.15
    
    return {
        "input_value": value,
        "input_unit": from_unit,
        "output_value": round(result, 4),
        "output_unit": to_unit,
        "category": "temperature"
    }


def convert_speed(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Convert speed between units."""
    if from_unit not in SPEED_UNITS or to_unit not in SPEED_UNITS:
        raise ValueError("Invalid speed unit")
    
    # Convert to m/s first, then to target unit
    mps = value * SPEED_UNITS[from_unit]
    result = mps / SPEED_UNITS[to_unit]
    
    return {
        "input_value": value,
        "input_unit": from_unit,
        "output_value": round(result, 6),
        "output_unit": to_unit,
        "category": "speed"
    }


def convert_data(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Convert digital data storage between units."""
    if from_unit not in DATA_UNITS or to_unit not in DATA_UNITS:
        raise ValueError("Invalid data unit")
    
    # Convert to bytes first, then to target unit
    bytes_val = value * DATA_UNITS[from_unit]
    result = bytes_val / DATA_UNITS[to_unit]
    
    return {
        "input_value": value,
        "input_unit": from_unit,
        "output_value": round(result, 6),
        "output_unit": to_unit,
        "category": "data"
    }


def get_available_units(category: str) -> List[str]:
    """Get list of available units for a category."""
    categories = {
        "length": list(LENGTH_UNITS.keys()),
        "weight": list(WEIGHT_UNITS.keys()),
        "temperature": TEMPERATURE_UNITS,
        "speed": list(SPEED_UNITS.keys()),
        "data": list(DATA_UNITS.keys())
    }
    return categories.get(category.lower(), [])


def convert(
    value: float,
    category: str,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """Generic convert function that routes to specific converters."""
    converters = {
        "length": convert_length,
        "weight": convert_weight,
        "temperature": convert_temperature,
        "speed": convert_speed,
        "data": convert_data
    }
    
    converter = converters.get(category.lower())
    if not converter:
        raise ValueError(f"Unknown category: {category}")
    
    return converter(value, from_unit, to_unit)
