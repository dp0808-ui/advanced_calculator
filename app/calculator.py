"""Main Calculator engine and REPL interface."""
import sys
from typing import List
from app.calculation import Calculation
from app.history import CalculationHistory
from app.calculator_memento import HistoryCareTaker
from app.operations import OperationFactory
from app.input_validators import InputValidator
from app.logger import LoggingObserver, AutoSaveObserver
from app.calculator_config import CalculatorConfig
from app.exceptions import CalculatorError

class Calculator:
    """Central Calculator engine implementing Observer, Memento, and Factory patterns."""

    def __init__(self):
        self.history_manager = CalculationHistory()
        self.caretaker = HistoryCareTaker()
        self.observers = [
            LoggingObserver(),
            AutoSaveObserver(self.history_manager)
        ]

    def notify_observers(self, calculation: Calculation):
        for observer in self.observers:
            observer.update(calculation)

    def calculate(self, operation_name: str, a: float, b: float) -> Calculation:
        self.caretaker.save_state(self.history_manager.get_history())
        calc = Calculation(operation_name, a, b)
        self.history_manager.add_calculation(calc)
        self.notify_observers(calc)
        return calc

    def undo(self) -> bool:
        prev_state = self.caretaker.undo(self.history_manager.get_history())
        if prev_state is not None:
            self.history_manager.set_history(prev_state)
            return True
        return False

    def redo(self) -> bool:
        next_state = self.caretaker.redo(self.history_manager.get_history())
        if next_state is not None:
            self.history_manager.set_history(next_state)
            return True
        return False


def parse_input(user_input: str):
    tokens = user_input.strip().split()
    if not tokens:
        return None, []
    return tokens[0].lower(), tokens[1:]


def repl():  # pragma: no cover
    calc_engine = Calculator()
    
    print("==========================================================")
    print("         ADVANCED OBJECT-ORIENTED CALCULATOR CLI          ")
    print("==========================================================")
    print("Operations: add, subtract, multiply, divide, power, root,")
    print("            modulus, int_divide, percent, abs_diff")
    print("Commands: history, clear, undo, redo, save, load, help, exit")
    print("==========================================================")

    while True:
        try:
            raw_input_data = input("calc> ")
            command, args = parse_input(raw_input_data)
            
            if not command:
                continue
            
            if command in ['exit', 'quit']:
                print("Exiting calculator session. Goodbye!")
                break
                
            elif command == 'help':
                print("\n--- Available Commands & Operations ---")
                print("Operations: ", ", ".join(OperationFactory.get_supported_operations()))
                print("System Cmds: history | clear | undo | redo | save | load | help | exit\n")
                continue
                
            elif command == 'history':
                history = calc_engine.history_manager.get_history()
                if not history:
                    print("History is empty.")
                else:
                    for idx, calc in enumerate(history, 1):
                        print(f"{idx}. {calc.operation_name}({calc.a}, {calc.b}) = {calc.result:.{CalculatorConfig.CALCULATOR_PRECISION}f}")
                continue
                
            elif command == 'clear':
                calc_engine.caretaker.save_state(calc_engine.history_manager.get_history())
                calc_engine.history_manager.clear()
                print("History cleared.")
                continue
                
            elif command == 'undo':
                if calc_engine.undo():
                    print("Undo successful.")
                else:
                    print("Nothing to undo.")
                continue
                
            elif command == 'redo':
                if calc_engine.redo():
                    print("Redo successful.")
                else:
                    print("Nothing to redo.")
                continue
                
            elif command == 'save':
                calc_engine.history_manager.save_to_csv()
                print(f"History saved to {CalculatorConfig.CALCULATOR_HISTORY_FILE}")
                continue
                
            elif command == 'load':
                calc_engine.history_manager.load_from_csv()
                print(f"History loaded from {CalculatorConfig.CALCULATOR_HISTORY_FILE}")
                continue
                
            if command in OperationFactory.get_supported_operations():
                validated_args = InputValidator.validate_arguments(args, 2)
                calculation = calc_engine.calculate(command, validated_args[0], validated_args[1])
                print(f"Result: {calculation.result:.{CalculatorConfig.CALCULATOR_PRECISION}f}")
            else:
                print(f"Syntax Error: Unknown command '{command}'. Type 'help' for options.")

        except CalculatorError as ce:
            print(f"Application Error: {ce}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting session. Goodbye!")
            break


if __name__ == "__main__":  # pragma: no cover
    repl()