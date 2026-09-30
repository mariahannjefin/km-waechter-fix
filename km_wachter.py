# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernised 2025.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return how many percent of the service interval have been used."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True when the car has reached or exceeded the warning threshold.

    A missing ``last_service_km`` is treated as the current odometer reading
    (i.e. the car is considered freshly serviced and not yet due).
    """
    last = car.get("last_service_km", car["odometer"])
    km_since = car["odometer"] - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list) -> list:
    """Flag every car that needs a service and return their ids."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
