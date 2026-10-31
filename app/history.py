"""Calculation history management and Pandas CSV persistence."""
from typing import List
from pathlib import Path
import pandas as pd
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError

class CalculationHistory:
    """Manages collection of calculation records with CSV serialization via pandas."""

    def __init__(self):
        self._history: List[Calculation] = []

    def add_calculation(self, calculation: Calculation):
        self._history.append(calculation)
        if len(self._history) > CalculatorConfig.CALCULATOR_MAX_HISTORY_SIZE:
            self._history.pop(0)

    def get_history(self) -> List[Calculation]:
        return list(self._history)

    def set_history(self, history: List[Calculation]):
        self._history = list(history)

    def clear(self):
        self._history.clear()

    def save_to_csv(self, filepath: str = None):
        path = filepath or CalculatorConfig.CALCULATOR_HISTORY_FILE
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            if not self._history:
                df = pd.DataFrame(columns=["operation", "operand_a", "operand_b", "result", "timestamp"])
            else:
                data = [calc.to_dict() for calc in self._history]
                df = pd.DataFrame(data)
            df.to_csv(path, index=False, encoding=CalculatorConfig.CALCULATOR_DEFAULT_ENCODING)
        except Exception as e:
            raise HistoryError(f"Failed to save history to CSV: {e}")

    def load_from_csv(self, filepath: str = None):
        path = filepath or CalculatorConfig.CALCULATOR_HISTORY_FILE
        if not Path(path).exists():
            raise HistoryError(f"History file '{path}' does not exist.")
        try:
            df = pd.read_csv(path, encoding=CalculatorConfig.CALCULATOR_DEFAULT_ENCODING)
            loaded = []
            for _, row in df.iterrows():
                calc_dict = {
                    "operation": row.get("operation", "add"),
                    "operand_a": row.get("operand_a", 0.0),
                    "operand_b": row.get("operand_b", 0.0),
                    "result": row.get("result", 0.0),
                    "timestamp": row.get("timestamp", "")
                }
                loaded.append(Calculation.from_dict(calc_dict))
            self._history = loaded
        except Exception as e:
            raise HistoryError(f"Failed to load history from CSV: {e}")