# fleet_report.py
# Prints the nightly fleet-health summary for Vossberg Mobility.
# Written in 2014. Modernised 2025.

from km_wachter import wear_percent, needs_service, SERVICE_INTERVAL_KM
from config_loader import load_settings, get_setting
from log_util import log, flush_log
import fleet_utils


def car_wear(car: dict) -> float:
    """Return wear percentage for a single car.

    Falls back to the current odometer when ``last_service_km`` is absent,
    meaning the car is treated as freshly serviced (0 % wear).
    """
    last = car.get("last_service_km", car["odometer"])
    return wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)


def fleet_summary(fleet: list) -> dict:
    """Return a summary dict with count, number due, and average wear."""
    total = 0.0
    due = 0
    for car in fleet:
        total += car_wear(car)
        if needs_service(car):
            due += 1
    average = total / len(fleet)
    return {"count": len(fleet), "due": due, "average_wear": average}


def print_report(fleet: list) -> None:
    """Print the nightly report to stdout and append a log entry."""
    settings = load_settings()
    log(get_setting(settings, "report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"Average wear: {s['average_wear']:.1f}%")
    total_km = sum(car["odometer"] for car in fleet)
    # The partner garage in England wants the distance in miles (since 2015).
    miles = fleet_utils.km_to_miles(total_km)
    print(f"Fleet distance: {fleet_utils.format_number(miles)} miles")
    flush_log(get_setting(settings, "log_file", "km_wachter.log"))
