"""Unit tests for Calculator engine, history, validators, memento, and observers."""
import pytest
from pathlib import Path
from app.calculator import Calculator, parse_input
from app.calculation import Calculation
from app.history import CalculationHistory
from app.calculator_memento import HistoryCareTaker
from app.input_validators import InputValidator
from app.exceptions import ValidationError, HistoryError, OperationError
from app.calculator_config import CalculatorConfig

def test_calculator_calculate_and_observers():
    calc = Calculator()
    res = calc.calculate("add", 10.0, 5.0)
    assert res.result == 15.0
    history = calc.history_manager.get_history()
    assert len(history) == 1

def test_calculator_undo_redo():
    calc = Calculator()
    calc.calculate("add", 1.0, 1.0)
    calc.calculate("add", 2.0, 2.0)
    assert len(calc.history_manager.get_history()) == 2

    assert calc.undo() is True
    assert len(calc.history_manager.get_history()) == 1

    assert calc.redo() is True
    assert len(calc.history_manager.get_history()) == 2

    assert calc.redo() is False
    assert calc.undo() is True
    assert calc.undo() is True
    assert calc.undo() is False

def test_input_validator_numbers():
    assert InputValidator.validate_number("123.45") == 123.45
    with pytest.raises(ValidationError):
        InputValidator.validate_number("abc")
    with pytest.raises(ValidationError):
        InputValidator.validate_number("2000000")

def test_input_validator_arguments():
    args = ["10", "20"]
    validated = InputValidator.validate_arguments(args, 2)
    assert validated == [10.0, 20.0]
    with pytest.raises(ValidationError):
        InputValidator.validate_arguments(["10"], 2)

def test_history_csv_persistence(tmp_path):
    history_file = tmp_path / "test_history.csv"
    history = CalculationHistory()
    calc = Calculation("multiply", 3.0, 4.0)
    history.add_calculation(calc)
    
    history.save_to_csv(str(history_file))
    assert history_file.exists()

    history2 = CalculationHistory()
    history2.load_from_csv(str(history_file))
    assert len(history2.get_history()) == 1
    assert history2.get_history()[0].result == 12.0

def test_history_load_nonexistent():
    history = CalculationHistory()
    with pytest.raises(HistoryError):
        history.load_from_csv("nonexistent_file_12345.csv")

def test_parse_input():
    cmd, args = parse_input("add 5 10")
    assert cmd == "add"
    assert args == ["5", "10"]

    assert parse_input("") == (None, [])