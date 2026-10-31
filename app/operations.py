"""Operation classes and Factory implementation for arithmetic calculations."""
from abc import ABC, abstractmethod
import math
from app.exceptions import OperationError

class Operation(ABC):
    """Abstract base class for all calculator operations."""

    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        pass


class Addition(Operation):
    def compute(self, a: float, b: float) -> float:
        return a + b


class Subtraction(Operation):
    def compute(self, a: float, b: float) -> float:
        return a - b


class Multiplication(Operation):
    def compute(self, a: float, b: float) -> float:
        return a * b


class Division(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Division by zero is undefined.")
        return a / b


class Power(Operation):
    def compute(self, a: float, b: float) -> float:
        try:
            res = math.pow(a, b)
            if math.isnan(res) or math.isinf(res):
                raise OperationError("Result of power operation is out of bounds.")
            return res
        except ValueError as e:
            raise OperationError(f"Invalid power operation: {e}")


class Root(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Zeroth root is undefined.")
        if a < 0 and b % 2 == 0:
            raise OperationError("Even root of a negative number is not real.")
        try:
            return math.pow(a, 1.0 / b)
        except ValueError as e:
            raise OperationError(f"Invalid root operation: {e}")


class Modulus(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Modulus by zero is undefined.")
        return math.fmod(a, b)


class IntegerDivision(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Integer division by zero is undefined.")
        return float(math.trunc(a / b))


class Percentage(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Percentage base cannot be zero.")
        return (a / b) * 100.0


class AbsoluteDifference(Operation):
    def compute(self, a: float, b: float) -> float:
        return abs(a - b)


class OperationFactory:
    """Factory pattern for creating and managing operation instances."""

    _registry = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root,
        'modulus': Modulus,
        'int_divide': IntegerDivision,
        'percent': Percentage,
        'abs_diff': AbsoluteDifference
    }

    @classmethod
    def create_operation(cls, name: str) -> Operation:
        op_name = name.lower()
        if op_name not in cls._registry:
            raise OperationError(f"Unknown operation: '{name}'.")
        return cls._registry[op_name]()

    @classmethod
    def get_supported_operations(cls) -> list:
        return list(cls._registry.keys())