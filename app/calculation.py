from datetime import datetime


class Calculation:
	def __init__(self, operation_name: str, a: float, b: float, result: float):
		self.operation_name = operation_name
		self.a = a
		self.b = b
		self.result = result
		self.timestamp = datetime.now()

	def to_dict(self):
		return {
			"operation": self.operation_name,
			"operand_a": self.a,
			"operand_b": self.b,
			"result": self.result,
			"timestamp": self.timestamp.isoformat(),
		}
