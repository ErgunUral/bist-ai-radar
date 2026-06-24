from __future__ import annotations

from .data_fetcher import FinancialStatements


class BistProvider:
    def __init__(self, provider_module=None):
        self.provider_module = provider_module

    def fetch(self, ticker: str) -> FinancialStatements:
        if self.provider_module is None:
            try:
                import borsapy as bp
            except ImportError as exc:
                raise ImportError("borsapy kurulu değil. pip install borsapy çalıştırın.") from exc
        else:
            bp = self.provider_module

        h = bp.Ticker(ticker.upper().strip())

        try:
            bs = h.quarterly_balance_sheet
        except Exception:
            bs = None
        try:
            inc = h.quarterly_income_stmt
        except Exception:
            inc = None
        try:
            cf = h.quarterly_cashflow
        except Exception:
            cf = None

        return FinancialStatements(balance_sheet=bs, income_statement=inc, cash_flow=cf)
