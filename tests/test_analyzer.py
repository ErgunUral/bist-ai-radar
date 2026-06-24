import pandas as pd

from src.analyzer import analyze_statements
from src.data_fetcher import FinancialStatements


def test_analyzer_selects_latest_period_and_scores():
    balance_sheet = pd.DataFrame(
        {
            "Q2/2026": [100, 300, 100, 1000, 400, 600, 100, 100],
            "Q3/2026": [150, 400, 150, 1200, 450, 750, 80, 120],
        },
        index=[
            "Nakit ve Nakit Benzerleri",
            "Dönen Varlıklar",
            "Kısa Vadeli Yükümlülükler",
            "Toplam Varlıklar",
            "Toplam Yükümlülükler",
            "Özkaynaklar",
            "Kısa Vadeli Borçlanmalar",
            "Uzun Vadeli Borçlanmalar",
        ],
    )
    income_statement = pd.DataFrame(
        {
            "Q2/2026": [500, 150, 100, 80],
            "Q3/2026": [700, 210, 140, 120],
        },
        index=["Hasılat", "Brüt Kar", "FAVÖK", "Net Dönem Karı"],
    )
    cash_flow = pd.DataFrame(
        {"Q2/2026": [70, -20], "Q3/2026": [100, -30]},
        index=["İşletme Faaliyetlerinden Nakit Akışları", "Maddi Duran Varlık Alımları"],
    )

    result = analyze_statements(
        "ASELS",
        FinancialStatements(balance_sheet, income_statement, cash_flow),
        market_value=1000,
    )

    assert result.period == "Q3/2026"
    assert result.ticker == "ASELS"
    assert 0 <= result.total_score <= 100
    assert result.decision
