from __future__ import annotations

from dataclasses import asdict, dataclass

from .ai_decision import build_warnings, decision_from_score, risk_label
from .financial_mapper import get_value
from .period_manager import latest_period
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


def analyze_statements(ticker: str, statements, market_value: float = 0.0) -> AnalysisResult:
    balance_sheet = statements.balance_sheet
    income_statement = statements.income_statement
    cash_flow = statements.cash_flow

    columns = []
    for frame in (balance_sheet, income_statement, cash_flow):
        if frame is not None and not frame.empty:
            columns.extend(list(frame.columns))

    period = latest_period(columns) or ""
    sector_type = classify_ticker(ticker)

    inputs = FinancialInputs(
        cash=get_value(balance_sheet, "cash", period),
        financial_investments=get_value(balance_sheet, "financial_investments", period),
        current_assets=get_value(balance_sheet, "current_assets", period),
        current_liabilities=get_value(balance_sheet, "current_liabilities", period),
        total_assets=get_value(balance_sheet, "total_assets", period),
        total_liabilities=get_value(balance_sheet, "total_liabilities", period),
        equity=get_value(balance_sheet, "equity", period),
        short_financial_debt=get_value(balance_sheet, "short_financial_debt", period),
        long_financial_debt=get_value(balance_sheet, "long_financial_debt", period),
        revenue=get_value(income_statement, "revenue", period),
        gross_profit=get_value(income_statement, "gross_profit", period),
        operating_profit=get_value(income_statement, "operating_profit", period),
        ebitda=get_value(income_statement, "ebitda", period),
        net_income=get_value(income_statement, "net_income", period),
        operating_cash_flow=get_value(cash_flow, "operating_cash_flow", period),
        capex=get_value(cash_flow, "capex", period),
        market_value=market_value,
    )

    ratios = calculate_ratios(inputs)
    metrics = ratios.to_dict()
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
