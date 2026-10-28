from copy import deepcopy

class CalculatorMemento:
    def __init__(self, history_state):
        self._state = deepcopy(history_state)

    def get_state(self):
        return deepcopy(self._state)
    