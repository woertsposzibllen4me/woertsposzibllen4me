"""Module for managing terminal windows."""

from .core.constants import TERMINAL_WINDOW_SLOTS_DB_FILE_PATH
from .core.twm_main import TerminalWindowManager
from .core.types import SecondaryWindow, WinType

__all__ = [
    "TERMINAL_WINDOW_SLOTS_DB_FILE_PATH",
    "SecondaryWindow",
    "TerminalWindowManager",
    "WinType",
]
