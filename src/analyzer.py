from __future__ import annotations

from dataclasses import asdict, dataclass

from .ai_decision import build_warnings, decision_from_score, risk_label
from .financial_mapper import get_value
from .period_manager import find_column_by_period, period_label_from_key, period_keys_from_tables
from .ratios import FinancialInputs, calculate_ratios
from .scoring import calculate_score
from .sector_rules import classify_ticker


@dataclass
class AnalysisResult:
    ticker: str
    period: str
    sector_type: str
    total_score: float
    decision: str
    risk: str
    warnings: str
    metrics: dict

    def to_dict(self) -> dict:
        base = asdict(self)
        metrics = base.pop("metrics")
        return {**base, **metrics}


def analyze_statements(ticker: str, statements, market_value: float = 0.0, target_periods: list[object] | None = None) -> AnalysisResult:
    balance_sheet = statements.balance_sheet
    income_statement = statements.income_statement
    cash_flow = statements.cash_flow

    period_keys = period_keys_from_tables(balance_sheet, income_statement, cash_flow, limit=999)
    if target_periods:
        from .period_manager import period_key_from_value
        wanted = {period_key_from_value(item) for item in target_periods}
        filtered = [key for key in period_keys if key in wanted]
        period_key = filtered[0] if filtered else (period_keys[0] if period_keys else (0, 0))
    else:
        period_key = period_keys[0] if period_keys else (0, 0)

    period = period_label_from_key(period_key)
    sector_type = classify_ticker(ticker)

    bs_col = find_column_by_period(balance_sheet, period_key)
    inc_col = find_column_by_period(income_statement, period_key)
    cf_col = find_column_by_period(cash_flow, period_key)

    inputs = FinancialInputs(
        cash=get_value(balance_sheet, "cash", bs_col),
        financial_investments=get_value(balance_sheet, "financial_investments", bs_col),
        current_assets=get_value(balance_sheet, "current_assets", bs_col),
        current_liabilities=get_value(balance_sheet, "current_liabilities", bs_col),
        total_assets=get_value(balance_sheet, "total_assets", bs_col),
        total_liabilities=get_value(balance_sheet, "total_liabilities", bs_col),
        equity=get_value(balance_sheet, "equity", bs_col),
        short_financial_debt=get_value(balance_sheet, "short_financial_debt", bs_col),
        long_financial_debt=get_value(balance_sheet, "long_financial_debt", bs_col),
        revenue=get_value(income_statement, "revenue", inc_col),
        gross_profit=get_value(income_statement, "gross_profit", inc_col),
        operating_profit=get_value(income_statement, "operating_profit", inc_col),
        ebitda=get_value(income_statement, "ebitda", inc_col),
        net_income=get_value(income_statement, "net_income", inc_col),
        operating_cash_flow=get_value(cash_flow, "operating_cash_flow", cf_col),
        capex=get_value(cash_flow, "capex", cf_col),
        market_value=market_value,
    )

    if not inputs.ebitda and inputs.operating_profit:
        depreciation = get_value(cash_flow, "depreciation_amortization", cf_col)
        inputs.ebitda = inputs.operating_profit + abs(depreciation)

    ratios = calculate_ratios(inputs)
    metrics = ratios.to_dict()
    metrics.update({
        "balance_sheet_column": str(bs_col) if bs_col is not None else "",
        "income_statement_column": str(inc_col) if inc_col is not None else "",
        "cash_flow_column": str(cf_col) if cf_col is not None else "",
    })
    score = calculate_score(metrics, sector_type)
    metrics.update(score.to_dict())

    return AnalysisResult(
        ticker=ticker.upper(),
        period=period,
        sector_type=str(sector_type),
        total_score=score.total_score,
        decision=decision_from_score(score.total_score),
        risk=risk_label(score.total_score),
        warnings=build_warnings(metrics),
        metrics=metrics,
    )
