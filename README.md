# Advanced Object-Oriented Calculator CLI

An enterprise-grade, extensible command-line calculator application built in Python. This application demonstrates advanced software engineering principles, robust error handling, automated CI/CD pipelines, and clean architectural design patterns.

---

## Features & Architecture

### 1. Design Patterns
* **Factory Pattern (`app/operations.py`)**: Dynamically manages and instantiates 10 arithmetic operations.
* **Memento Pattern (`app/calculator_memento.py`)**: Snapshots calculation history states to support full **Undo** and **Redo** capabilities.
* **Observer Pattern (`app/logger.py`)**: Automatically triggers event-driven side effects, including file logging and pandas CSV history auto-saving.

### 2. Supported Operations & Commands
* **Arithmetic Operations**:
  * `add`, `subtract`, `multiply`, `divide`
  * `power`, `root`, `modulus`, `int_divide`
  * `percent`, `abs_diff`
* **System Commands**:
  * `history` – View previous calculations with timestamps and precision formatting.
  * `undo` / `redo` – Navigate through history states.
  * `clear` – Clear active calculation history.
  * `save` / `load` – Manually serialize/deserialize history to/from CSV via `pandas`.
  * `help` – Display instructions.
  * `exit` – Terminate the application gracefully.

### 3. Configuration Management (`.env`)
Configured using `python-dotenv` with robust fallback defaults:
* `CALCULATOR_LOG_DIR`: Directory for application logs (`logs/`).
* `CALCULATOR_HISTORY_DIR`: Directory for CSV persistence (`history/`).
* `CALCULATOR_MAX_HISTORY_SIZE`: Maximum rolling history entry limit.
* `CALCULATOR_AUTO_SAVE`: Enables/disables automated CSV saving on calculation.
* `CALCULATOR_PRECISION`: Decimal display precision.
* `CALCULATOR_MAX_INPUT_VALUE`: Maximum allowable numeric input limit.

---

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/your-username/advanced_calculator.git](https://github.com/your-username/advanced_calculator.git)
   cd advanced_calculator