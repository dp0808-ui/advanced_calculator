"""Memento pattern implementation for Undo/Redo state management."""
from typing import List, Optional
from copy import deepcopy
from app.calculation import Calculation

class CalculatorMemento:
    """Stores a snapshot of calculation history."""
    def __init__(self, state: List[Calculation]):
        self._state = deepcopy(state)

    def get_state(self) -> List[Calculation]:
        return deepcopy(self._state)


class HistoryCareTaker:
    """Manages undo and redo stacks using CalculatorMemento."""

    def __init__(self):
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

    def save_state(self, current_state: List[Calculation]):
        self._undo_stack.append(CalculatorMemento(current_state))
        self._redo_stack.clear()

    def undo(self, current_state: List[Calculation]) -> Optional[List[Calculation]]:
        if not self._undo_stack:
            return None
        self._redo_stack.append(CalculatorMemento(current_state))
        memento = self._undo_stack.pop()
        return memento.get_state()

    def redo(self, current_state: List[Calculation]) -> Optional[List[Calculation]]:
        if not self._redo_stack:
            return None
        self._undo_stack.append(CalculatorMemento(current_state))
        memento = self._redo_stack.pop()
        return memento.get_state()