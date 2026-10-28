from app.calculator_memento import CalculatorMemento

class HistoryManager:
    def __init__(self, max_size: int = 100):
        self._history = []
        self._max_size = max_size
        self._undo_stack = []
        self._redo_stack = []

    def add_calculation(self, calculation):
        # Save current state for undo before modifying
        self._undo_stack.append(self.save_memento())
        self._redo_stack.clear()  # Clear redo on new action
        
        self._history.append(calculation)
        if len(self._history) > self._max_size:
            self._history.pop(0)

    def save_memento(self) -> CalculatorMemento:
        return CalculatorMemento(self._history)

    def restore_memento(self, memento: CalculatorMemento):
        self._history = memento.get_state()

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        self._redo_stack.append(self.save_memento())
        memento = self._undo_stack.pop()
        self.restore_memento(memento)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        self._undo_stack.append(self.save_memento())
        memento = self._redo_stack.pop()
        self.restore_memento(memento)
        return True

    def get_history(self):
        return self._history

    def clear(self):
        self._undo_stack.append(self.save_memento())
        self._redo_stack.clear()
        self._history.clear()