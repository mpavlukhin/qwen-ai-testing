"""
Health calculator logic.
Pure functions for health-related calculations.
"""

from typing import Dict, Any


def calculate_bmi(weight_kg: float, height_cm: float) -> Dict[str, Any]:
    """
    Calculate Body Mass Index (BMI).
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
    
    Returns:
        Dictionary with BMI value and category
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
        health_risk = "Low (but risk of other nutritional deficiencies)"
    elif bmi < 25:
        category = "Normal weight"
        health_risk = "Average"
    elif bmi < 30:
        category = "Overweight"
        health_risk = "Increased"
    elif bmi < 35:
        category = "Obese Class I"
        health_risk = "High"
    elif bmi < 40:
        category = "Obese Class II"
        health_risk = "Very High"
    else:
        category = "Obese Class III"
        health_risk = "Extremely High"
    
    return {
        "bmi": round(bmi, 2),
        "category": category,
        "health_risk": health_risk,
        "weight_kg": weight_kg,
        "height_cm": height_cm
    }


def calculate_bmr(
    weight_kg: float,
    height_cm: float,
    age: int,
    gender: str
) -> Dict[str, float]:
    """
    Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor equation.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        gender: 'male' or 'female'
    
    Returns:
        Dictionary with BMR and daily calorie needs for different activity levels
    """
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    # Activity level multipliers
    activity_levels = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extra_active": 1.9
    }
    
    daily_calories = {
        level: round(bmr * multiplier, 2)
        for level, multiplier in activity_levels.items()
    }
    
    return {
        "bmr": round(bmr, 2),
        "daily_calories": daily_calories,
        "gender": gender,
        "age": age,
        "weight_kg": weight_kg,
        "height_cm": height_cm
    }


def calculate_daily_water_intake(
    weight_kg: float,
    activity_minutes: int = 0,
    climate: str = "normal"
) -> Dict[str, float]:
    """
    Calculate recommended daily water intake.
    
    Args:
        weight_kg: Weight in kilograms
        activity_minutes: Minutes of physical activity per day
        climate: 'normal', 'hot', or 'cold'
    
    Returns:
        Dictionary with recommended water intake in liters
    """
    # Base recommendation: 30-35 ml per kg of body weight
    base_intake = weight_kg * 0.033
    
    # Add water for exercise (12 oz per 30 min ≈ 0.35 L per 30 min)
    exercise_intake = (activity_minutes / 30) * 0.35
    
    # Climate adjustment
    climate_multipliers = {
        "normal": 1.0,
        "hot": 1.2,
        "cold": 0.95
    }
    multiplier = climate_multipliers.get(climate.lower(), 1.0)
    
    total_intake = (base_intake + exercise_intake) * multiplier
    
    return {
        "recommended_liters": round(total_intake, 2),
        "base_intake": round(base_intake, 2),
        "exercise_intake": round(exercise_intake, 2),
        "climate_adjustment": multiplier,
        "weight_kg": weight_kg,
        "activity_minutes": activity_minutes,
        "climate": climate
    }


def calculate_tdee(
    weight_kg: float,
    height_cm: float,
    age: int,
    gender: str,
    activity_level: str
) -> Dict[str, Any]:
    """
    Calculate Total Daily Energy Expenditure (TDEE).
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        gender: 'male' or 'female'
        activity_level: One of 'sedentary', 'lightly_active', 'moderately_active', 
                       'very_active', 'extra_active'
    
    Returns:
        Dictionary with TDEE and calorie goals for weight loss/gain
    """
    # Calculate BMR first
    bmr_result = calculate_bmr(weight_kg, height_cm, age, gender)
    bmr = bmr_result["bmr"]
    
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extra_active": 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
    tdee = bmr * multiplier
    
    # Calorie goals
    mild_weight_loss = tdee - 250
    weight_loss = tdee - 500
    extreme_weight_loss = tdee - 1000
    mild_weight_gain = tdee + 250
    weight_gain = tdee + 500
    extreme_weight_gain = tdee + 1000
    
    return {
        "tdee": round(tdee, 2),
        "bmr": bmr,
        "activity_level": activity_level,
        "goals": {
            "mild_weight_loss_0_25kg_week": round(mild_weight_loss, 2),
            "weight_loss_0_5kg_week": round(weight_loss, 2),
            "extreme_weight_loss_1kg_week": round(extreme_weight_loss, 2),
            "maintain_weight": round(tdee, 2),
            "mild_weight_gain_0_25kg_week": round(mild_weight_gain, 2),
            "weight_gain_0_5kg_week": round(weight_gain, 2),
            "extreme_weight_gain_1kg_week": round(extreme_weight_gain, 2)
        }
    }
