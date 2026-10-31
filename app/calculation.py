"""Represents an individual calculation record."""
from datetime import datetime
from app.exceptions import OperationError

class Calculation:
    """Encapsulates operands, operation name, result, and timestamp."""

    def __init__(self, operation_name: str, a: float, b: float):
        self.operation_name = operation_name.lower()
        self.a = float(a)
        self.b = float(b)
        self.timestamp = datetime.now()
        self.result = self._execute()

    def _execute(self) -> float:
        from app.operations import OperationFactory
        op = OperationFactory.create_operation(self.operation_name)
        return op.compute(self.a, self.b)

    def to_dict(self) -> dict:
        return {
            "operation": self.operation_name,
            "operand_a": self.a,
            "operand_b": self.b,
            "result": self.result,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Calculation':
        calc = cls(data["operation"], data["operand_a"], data["operand_b"])
        if "timestamp" in data and data["timestamp"]:
            try:
                calc.timestamp = datetime.fromisoformat(str(data["timestamp"]))
            except ValueError:
                pass
        if "result" in data:
            try:
                calc.result = float(data["result"])
            except (ValueError, TypeError):
                pass
        return calc

    def __repr__(self) -> str:
        return f"Calculation({self.operation_name}, {self.a}, {self.b}) = {self.result}"