# log_util.py
# A homemade logger. Modernised 2025.

import time

LOG_LINES: list[str] = []       # module-level buffer, flushed by flush_log()
DEBUG = False


def log(message: str) -> None:
    """Append a timestamped line to the buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log at DEBUG level (only active when DEBUG is True)."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Write buffered log lines to *path* (append mode) and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
