# config_loader.py
# Reads settings.cfg. Hand-rolled in 2013. Modernised 2025.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Parse *path* (default: settings.cfg) and return a dict of known keys.

    Unknown keys are silently skipped — a typo in the cfg file will never
    surface, which is a known limitation inherited from the 2013 design.
    """
    if path is None:
        path = SETTINGS_FILE
    settings: dict[str, str] = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return the integer value for *key*, or *fallback* if absent/invalid."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return the string value for *key*, or *fallback* if absent."""
    return settings.get(key, fallback)
