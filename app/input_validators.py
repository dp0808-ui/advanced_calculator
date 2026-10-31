"""Input validation utilities for numeric inputs and command arguments."""
from app.exceptions import ValidationError
from app.calculator_config import CalculatorConfig

class InputValidator:
    """Validates command-line arguments and numeric ranges."""

    @staticmethod
    def validate_number(value_str: str) -> float:
        try:
            val = float(value_str)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid numeric input: '{value_str}' is not a valid number.")
        
        if abs(val) > CalculatorConfig.CALCULATOR_MAX_INPUT_VALUE:
            raise ValidationError(f"Input value {val} exceeds maximum allowed limit of {CalculatorConfig.CALCULATOR_MAX_INPUT_VALUE}.")
        return val

    @staticmethod
    def validate_arguments(args: list, expected_count: int = 2) -> list:
        if len(args) < expected_count:
            raise ValidationError(f"Missing arguments: Expected {expected_count}, got {len(args)}.")
        
        validated = []
        for i in range(expected_count):
            validated.append(InputValidator.validate_number(args[i]))
        return validated