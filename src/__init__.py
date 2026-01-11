"""Project root level package."""

from src.core.constants import COMMON_LOGS_FILE_PATH, LOG_DIR_PATH

if not LOG_DIR_PATH.exists():
    print(f"[src.__init__] Creating log directory at {LOG_DIR_PATH}")
    LOG_DIR_PATH.mkdir(parents=True, exist_ok=True)

with COMMON_LOGS_FILE_PATH.open("a") as log_file:
    log_file.write("<< New Log Entry >>\n")
    print(f"[src.__init__] New log entry written to {COMMON_LOGS_FILE_PATH}")
