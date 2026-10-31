"""Configuration management module utilizing python-dotenv."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class CalculatorConfig:
    """Central configuration class with validation and default fallback values."""
    
    CALCULATOR_LOG_DIR: str = os.getenv("CALCULATOR_LOG_DIR", "logs")
    CALCULATOR_HISTORY_DIR: str = os.getenv("CALCULATOR_HISTORY_DIR", "history")
    
    Path(CALCULATOR_LOG_DIR).mkdir(parents=True, exist_ok=True)
    Path(CALCULATOR_HISTORY_DIR).mkdir(parents=True, exist_ok=True)
    
    CALCULATOR_LOG_FILE: str = str(Path(CALCULATOR_LOG_DIR) / "calculator.log")
    CALCULATOR_HISTORY_FILE: str = str(Path(CALCULATOR_HISTORY_DIR) / "history.csv")
    
    try:
        CALCULATOR_MAX_HISTORY_SIZE: int = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
    except ValueError:
        CALCULATOR_MAX_HISTORY_SIZE = 100

    try:
        CALCULATOR_AUTO_SAVE: bool = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() in ("true", "1", "yes")
    except ValueError:
        CALCULATOR_AUTO_SAVE = True

    try:
        CALCULATOR_PRECISION: int = int(os.getenv("CALCULATOR_PRECISION", "4"))
    except ValueError:
        CALCULATOR_PRECISION = 4

    try:
        CALCULATOR_MAX_INPUT_VALUE: float = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000.0"))
    except ValueError:
        CALCULATOR_MAX_INPUT_VALUE = 1000000.0

    CALCULATOR_DEFAULT_ENCODING: str = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")