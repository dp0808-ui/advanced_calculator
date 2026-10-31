"""Unit tests for operations and operation factory."""
import pytest
from app.operations import OperationFactory
from app.exceptions import OperationError

@pytest.mark.parametrize("op_name, a, b, expected", [
    ("add", 2.0, 3.0, 5.0),
    ("subtract", 5.0, 2.0, 3.0),
    ("multiply", 4.0, 3.0, 12.0),
    ("divide", 10.0, 2.0, 5.0),
    ("power", 2.0, 3.0, 8.0),
    ("root", 8.0, 3.0, 2.0),
    ("modulus", 10.0, 3.0, 1.0),
    ("int_divide", 7.0, 2.0, 3.0),
    ("percent", 50.0, 200.0, 25.0),
    ("abs_diff", 3.0, 7.0, 4.0)
])
def test_operations_success(op_name, a, b, expected):
    op = OperationFactory.create_operation(op_name)
    assert op.compute(a, b) == pytest.approx(expected)

def test_division_by_zero():
    op = OperationFactory.create_operation("divide")
    with pytest.raises(OperationError):
        op.compute(5.0, 0.0)

def test_modulus_by_zero():
    op = OperationFactory.create_operation("modulus")
    with pytest.raises(OperationError):
        op.compute(5.0, 0.0)

def test_int_division_by_zero():
    op = OperationFactory.create_operation("int_divide")
    with pytest.raises(OperationError):
        op.compute(5.0, 0.0)

def test_percentage_by_zero():
    op = OperationFactory.create_operation("percent")
    with pytest.raises(OperationError):
        op.compute(5.0, 0.0)

def test_root_invalid():
    op = OperationFactory.create_operation("root")
    with pytest.raises(OperationError):
        op.compute(8.0, 0.0)
    with pytest.raises(OperationError):
        op.compute(-4.0, 2.0)

def test_unknown_operation():
    with pytest.raises(OperationError):
        OperationFactory.create_operation("nonexistent")

def test_get_supported_operations():
    supported = OperationFactory.get_supported_operations()
    assert "add" in supported
    assert "power" in supported