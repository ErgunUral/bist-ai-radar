from src.ratios import FinancialInputs, calculate_ratios


def test_basic_ratios():
    ratios = calculate_ratios(FinancialInputs(
        current_assets=200,
        current_liabilities=100,
        equity=500,
        total_liabilities=250,
        net_income=100,
        total_assets=1000,
    ))

    assert ratios.current_ratio == 2
    assert ratios.roe == 20
