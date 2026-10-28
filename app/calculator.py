import pandas as pd
from app.operations import OperationFactory
from app.calculation import Calculation
from app.history import HistoryManager
from app.calculator_config import Config
from app.logger import LoggingObserver, AutoSaveObserver
from app.exceptions import HistoryError

class Calculator:
    def __init__(self):
        Config.validate_and_setup()
        self.history_manager = HistoryManager(max_size=Config.MAX_HISTORY_SIZE)
        self.observers = [
            LoggingObserver(),
            AutoSaveObserver(self.history_manager)
        ]

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, calculation):
        for observer in self.observers:
            observer.update(calculation)

    def compute(self, op_name: str, a: float, b: float) -> float:
        operation = OperationFactory.create_operation(op_name)
        result = round(operation.execute(a, b), Config.PRECISION)
        
        calc = Calculation(op_name, a, b, result)
        self.history_manager.add_calculation(calc)
        self.notify_observers(calc)
        return result

    def undo(self) -> bool:
        return self.history_manager.undo()

    def redo(self) -> bool:
        return self.history_manager.redo()

    def clear_history(self):
        self.history_manager.clear()

    def get_history_records(self):
        return self.history_manager.get_history()

    def save_history_to_file(self, filename: str = None):
        path = Config.HISTORY_DIR / (filename or "history.csv")
        try:
            data = [c.to_dict() for c in self.get_history_records()]
            df = pd.DataFrame(data)
            df.to_csv(path, index=False, encoding=Config.DEFAULT_ENCODING)
        except Exception as e:
            raise HistoryError(f"Failed to save history: {e}")

    def load_history_from_file(self, filename: str = None):
        path = Config.HISTORY_DIR / (filename or "history.csv")
        try:
            if not path.exists():
                raise HistoryError("History file does not exist.")
            df = pd.read_csv(path, encoding=Config.DEFAULT_ENCODING)
            self.history_manager.clear()
            for _, row in df.iterrows():
                calc = Calculation(row["operation"], row["operand_a"], row["operand_b"], row["result"])
                self.history_manager.add_calculation(calc)
        except Exception as e:
            raise HistoryError(f"Failed to load history: {e}")