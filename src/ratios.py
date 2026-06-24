"""Financial ratio calculations."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class FinancialInputs:
    cash: float = 0.0
    financial_investments: float = 0.0
    current_assets: float = 0.0
    current_liabilities: float = 0.0
    total_assets: float = 0.0
    total_liabilities: float = 0.0
    equity: float = 0.0
    short_financial_debt: float = 0.0
    long_financial_debt: float = 0.0
    revenue: float = 0.0
    gross_profit: float = 0.0
    operating_profit: float = 0.0
    ebitda: float = 0.0
    net_income: float = 0.0
    operating_cash_flow: float = 0.0
    capex: float = 0.0
    market_value: float = 0.0


@dataclass
class FinancialRatios:
    net_working_capital: float = 0.0
    total_financial_debt: float = 0.0
    net_debt: float = 0.0
    enterprise_value: float = 0.0
    current_ratio: float | None = None
    debt_to_equity: float | None = None
    net_debt_to_ebitda: float | None = None
    gross_margin: float | None = None
    ebitda_margin: float | None = None
    net_margin: float | None = None
    roe: float | None = None
    roa: float | None = None
    price_to_book: float | None = None
    price_to_earnings: float | None = None
    ev_to_ebitda: float | None = None
    free_cash_flow: float = 0.0

    def to_dict(self) -> dict[str, float | None]:
        return asdict(self)


def safe_divide(numerator: float, denominator: float) -> float | None:
    if denominator in (0, 0.0) or denominator is None:
        return None
    return numerator / denominator


def percent(numerator: float, denominator: float) -> float | None:
    value = safe_divide(numerator, denominator)
    return None if value is None else value * 100


def calculate_ratios(values: FinancialInputs) -> FinancialRatios:
    total_financial_debt = values.short_financial_debt + values.long_financial_debt
    cash_like = values.cash + values.financial_investments
    net_debt = total_financial_debt - cash_like
    enterprise_value = values.market_value + net_debt if values.market_value else 0.0
    free_cash_flow = values.operating_cash_flow - abs(values.capex)

    return FinancialRatios(
        net_working_capital=values.current_assets - values.current_liabilities,
        total_financial_debt=total_financial_debt,
        net_debt=net_debt,
        enterprise_value=enterprise_value,
        current_ratio=safe_divide(values.current_assets, values.current_liabilities),
        debt_to_equity=safe_divide(values.total_liabilities, values.equity),
        net_debt_to_ebitda=safe_divide(net_debt, values.ebitda),
        gross_margin=percent(values.gross_profit, values.revenue),
        ebitda_margin=percent(values.ebitda, values.revenue),
        net_margin=percent(values.net_income, values.revenue),
        roe=percent(values.net_income, values.equity),
        roa=percent(values.net_income, values.total_assets),
        price_to_book=safe_divide(values.market_value, values.equity),
        price_to_earnings=safe_divide(values.market_value, values.net_income),
        ev_to_ebitda=safe_divide(enterprise_value, values.ebitda),
        free_cash_flow=free_cash_flow,
    )
