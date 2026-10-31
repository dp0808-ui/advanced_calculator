"""Observer pattern implementation for logging and auto-saving calculation events."""
from abc import ABC, abstractmethod
import logging
from pathlib import Path
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.history import CalculationHistory

Path(CalculatorConfig.CALCULATOR_LOG_DIR).mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=CalculatorConfig.CALCULATOR_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding=CalculatorConfig.CALCULATOR_DEFAULT_ENCODING
)

class Observer(ABC):
    """Abstract Observer interface."""
    @abstractmethod
    def update(self, calculation: Calculation):
        pass


class LoggingObserver(Observer):
    """Logs calculation details to the configured log file."""
    def update(self, calculation: Calculation):
        logging.info(
            f"Operation: {calculation.operation_name} | "
            f"Operands: ({calculation.a}, {calculation.b}) | "
            f"Result: {calculation.result}"
        )


class AutoSaveObserver(Observer):
    """Automatically saves calculation history to CSV when enabled."""
    def __init__(self, history_manager: CalculationHistory):
        self.history_manager = history_manager

    def update(self, calculation: Calculation):
        if CalculatorConfig.CALCULATOR_AUTO_SAVE:
            try:
                self.history_manager.save_to_csv()
            except Exception as e:
                logging.error(f"AutoSave failed: {e}")