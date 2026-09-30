# test_km_wachter.py
from km_wachter import needs_service, wear_percent, SERVICE_INTERVAL_KM, WARN_AT_PERCENT


def test_almost_due_car_is_flagged():
    # A car at 14,900 of its 15,000 km window is about 99% worn and MUST be flagged.
    assert needs_service({"id": "VOS-4471", "odometer": 14900, "last_service_km": 0}) is True


def test_missing_reading_is_not_treated_as_zero():
    # A car with NO last-service reading must not be treated as fully worn.
    assert needs_service({"id": "VOS-7788", "odometer": 92000}) is False


def test_wear_percent_uses_true_division():
    # 12,000 km of a 15,000 km interval = exactly 80 % (the warning threshold).
    # Integer division would give 0 * 100 = 0, so this test validates true / is used.
    result = wear_percent(12000, SERVICE_INTERVAL_KM)
    assert result == 80.0


def test_wear_percent_below_threshold():
    # 11,999 km just under the 12,000 km warning mark must be below 80 %.
    result = wear_percent(11999, SERVICE_INTERVAL_KM)
    assert result < WARN_AT_PERCENT


def test_wear_percent_above_threshold():
    # 15,000 km = 100 % — definitely due.
    result = wear_percent(15000, SERVICE_INTERVAL_KM)
    assert result == 100.0
