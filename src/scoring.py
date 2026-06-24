"""Sector-aware scoring engine."""

from __future__ import annotations

from dataclasses import dataclass, asdict

from .sector_rules import SectorType, get_score_weights


@dataclass
class ScoreBreakdown:
    financial_health: float = 0.0
    profitability: float = 0.0
    growth: float = 0.0
    cash_flow: float = 0.0
    leverage: float = 0.0
    valuation: float = 0.0
    total_score: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def score_bool(condition: bool, points: float) -> float:
    return points if condition else 0.0


def calculate_score(metrics: dict, sector_type: SectorType = SectorType.INDUSTRIAL) -> ScoreBreakdown:
    weights = get_score_weights(sector_type)

    current_ratio = metrics.get("current_ratio")
    debt_to_equity = metrics.get("debt_to_equity")
    net_margin = metrics.get("net_margin")
    ebitda_margin = metrics.get("ebitda_margin")
    roe = metrics.get("roe")
    roa = metrics.get("roa")
    revenue_growth = metrics.get("revenue_growth")
    net_income_growth = metrics.get("net_income_growth")
    free_cash_flow = metrics.get("free_cash_flow")
    net_debt = metrics.get("net_debt")
    price_to_earnings = metrics.get("price_to_earnings")
    price_to_book = metrics.get("price_to_book")

    financial_health = 0.0
    financial_health += score_bool(current_ratio is not None and current_ratio >= 1.5, weights["financial_health"] * 0.45)
    financial_health += score_bool(debt_to_equity is not None and debt_to_equity <= 1.5, weights["financial_health"] * 0.35)
    financial_health += score_bool(net_debt is not None and net_debt <= 0, weights["financial_health"] * 0.20)

    profitability = 0.0
    profitability += score_bool(roe is not None and roe >= 20, weights["profitability"] * 0.40)
    profitability += score_bool(roa is not None and roa >= 8, weights["profitability"] * 0.20)
    profitability += score_bool(net_margin is not None and net_margin >= 10, weights["profitability"] * 0.20)
    profitability += score_bool(ebitda_margin is not None and ebitda_margin >= 15, weights["profitability"] * 0.20)

    growth = 0.0
    growth += score_bool(revenue_growth is not None and revenue_growth > 0, weights["growth"] * 0.45)
    growth += score_bool(net_income_growth is not None and net_income_growth > 0, weights["growth"] * 0.55)

    cash_flow = score_bool(free_cash_flow is not None and free_cash_flow > 0, weights["cash_flow"])

    leverage = 0.0
    leverage += score_bool(debt_to_equity is not None and debt_to_equity <= 1, weights["leverage"] * 0.60)
    leverage += score_bool(net_debt is not None and net_debt <= 0, weights["leverage"] * 0.40)

    valuation = 0.0
    valuation += score_bool(price_to_earnings is not None and 0 < price_to_earnings <= 15, weights["valuation"] * 0.55)
    valuation += score_bool(price_to_book is not None and 0 < price_to_book <= 2, weights["valuation"] * 0.45)

    total = financial_health + profitability + growth + cash_flow + leverage + valuation
    return ScoreBreakdown(
        financial_health=round(clamp(financial_health), 2),
        profitability=round(clamp(profitability), 2),
        growth=round(clamp(growth), 2),
        cash_flow=round(clamp(cash_flow), 2),
        leverage=round(clamp(leverage), 2),
        valuation=round(clamp(valuation), 2),
        total_score=round(clamp(total), 2),
    )
