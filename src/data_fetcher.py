"""Data fetcher interface for financial statements.

The concrete BIST provider integration will be connected from the notebook layer.
This module keeps the project testable by separating provider-specific code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


@dataclass
class FinancialStatements:
    balance_sheet: pd.DataFrame | None = None
    income_statement: pd.DataFrame | None = None
    cash_flow: pd.DataFrame | None = None


class FinancialDataProvider(Protocol):
    def fetch(self, ticker: str) -> FinancialStatements:
        """Fetch financial statements for a ticker."""


class EmptyProvider:
    """Fallback provider used in tests and examples."""

    def fetch(self, ticker: str) -> FinancialStatements:
        return FinancialStatements()
