# fleet_utils.py
# Catch-all helpers since 2013. Modernised 2025.

# Correct value: 1 km = 0.621371 miles.
# The original file had 1.609 (which is km-per-mile, the inverse), making every
# UK mileage figure ~2.6× too large.
MILES_PER_KM = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a value as a whole-number percentage string."""
    return f"{value:.0f}%"


def mean(values: list) -> float:
    """Return the arithmetic mean of *values*, or 0 for an empty list."""
    total = 0.0
    count = 0
    for v in values:
        total += v
        count += 1
    if count == 0:
        return 0.0
    return total / count


def is_due(pct: float, threshold: float) -> bool:
    """Return True when *pct* has reached or exceeded *threshold*."""
    return pct >= threshold


def parse_service_date(text: str) -> tuple | None:
    """Parse a DD.MM.YYYY string into a (year, month, day) tuple, or None."""
    parts = text.split(".")
    if len(parts) != 3:
        return None
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    return (year, month, day)


def chunk_list(items: list, size: int) -> list:
    """Split *items* into sub-lists of length *size*."""
    chunks = []
    current: list = []
    for item in items:
        current.append(item)
        if len(current) == size:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks
