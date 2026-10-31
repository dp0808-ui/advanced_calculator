"""
Custom exception classes for the calculator application.
"""

class CalculatorError(Exception):
    """Base exception for all calculator-related errors."""
    pass

class OperationError(CalculatorError):
    """Raised when an arithmetic operation fails (e.g., division by zero)."""
    pass

class ValidationError(CalculatorError):
    """Raised when user inputs are invalid or out of allowed ranges."""
    pass

class HistoryError(CalculatorError):
    """Raised when an error occurs while managing history or undo/redo stacks."""
    pass