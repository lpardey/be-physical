import math
from enum import StrEnum


class BMICategory(StrEnum):
    """
    Based on the World Health Organization (WHO) guidelines
    """

    UNDERWEIGHT = "underweight"
    HEALTHY_WEIGHT = "healthy weight"
    OVERWEIGHT = "overweight"
    OBESITY_CLASS_I = "obesity (class I)"
    OBESITY_CLASS_II = "obesity (class II)"
    OBESITY_CLASS_III = "obesity (class III)"


BMI_CATEGORY_BOUNDS = {
    BMICategory.UNDERWEIGHT: 18.5,
    BMICategory.HEALTHY_WEIGHT: 25.0,
    BMICategory.OVERWEIGHT: 30.0,
    BMICategory.OBESITY_CLASS_I: 35.0,
    BMICategory.OBESITY_CLASS_II: 40.0,
    BMICategory.OBESITY_CLASS_III: math.inf,
}


def get_category_name(bmi: float) -> str:
    result = "unknown"

    for category, bound in BMI_CATEGORY_BOUNDS.items():
        if bmi < bound:
            result = category.value
            break

    return result


def get_bmi(height: float, weight: float) -> float:
    return round(weight / (height**2), 2)
