from src.scoring import calculate_score
from src.sector_rules import SectorType


def test_score_range():
    result = calculate_score({
        "roe": 25,
        "current_ratio": 2,
        "debt_to_equity": 0.5,
        "net_debt": -100,
        "free_cash_flow": 100,
    }, SectorType.INDUSTRIAL)

    assert 0 <= result.total_score <= 100
