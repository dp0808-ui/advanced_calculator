import logging
from abc import ABC, abstractmethod
import pandas as pd
from app.calculator_config import Config

class Observer(ABC):
    @abstractmethod
    def update(self, calculation):
        pass

class LoggingObserver(Observer):
    def __init__(self):
        Config.validate_and_setup()
        log_file = Config.LOG_DIR / "calculator.log"
        
        self.logger = logging.getLogger("CalculatorLogger")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file, encoding=Config.DEFAULT_ENCODING)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def update(self, calculation):
        msg = f"Op: {calculation.operation_name}, Operands: ({calculation.a}, {calculation.b}), Result: {calculation.result}"
        self.logger.info(msg)

class AutoSaveObserver(Observer):
    def __init__(self, history_manager):
        self.history_manager = history_manager
        Config.validate_and_setup()
        self.history_file = Config.HISTORY_DIR / "history.csv"

    def update(self, calculation):
        if Config.AUTO_SAVE:
            self.save_to_csv()

    def save_to_csv(self):
        data = [c.to_dict() for c in self.history_manager.get_history()]
        if data:
            df = pd.DataFrame(data)
            df.to_csv(self.history_file, index=False, encoding=Config.DEFAULT_ENCODING)