from src.period_manager import latest_period, select_recent_periods


def test_latest_period():
    periods = ["Q2/2025", "Q1/2026", "Q3/2026"]
    assert latest_period(periods) == "Q3/2026"


def test_recent_periods():
    periods = ["Q2/2025", "Q4/2025", "Q1/2026", "Q3/2026", "Q2/2026"]
    assert select_recent_periods(periods, 2) == ["Q3/2026", "Q2/2026"]
