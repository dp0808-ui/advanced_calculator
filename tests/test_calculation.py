"""Unit tests for Calculation model."""
import pytest
from app.calculation import Calculation
from app.exceptions import OperationError

def test_calculation_creation():
    calc = Calculation("add", 5.0, 3.0)
    assert calc.operation_name == "add"
    assert calc.a == 5.0
    assert calc.b == 3.0
    assert calc.result == 8.0

def test_calculation_to_and_from_dict():
    calc = Calculation("multiply", 4.0, 2.0)
    d = calc.to_dict()
    assert d["operation"] == "multiply"
    assert d["operand_a"] == 4.0
    assert d["operand_b"] == 2.0
    assert d["result"] == 8.0

    calc_restored = Calculation.from_dict(d)
    assert calc_restored.operation_name == "multiply"
    assert calc_restored.result == 8.0

def test_calculation_repr():
    calc = Calculation("subtract", 10.0, 4.0)
    assert "Calculation" in repr(calc)