from __future__ import annotations

from .data_fetcher import FinancialStatements


class BistProvider:
    """Adapter shell for the financial data provider used by the Colab notebook.

    The notebook will connect the concrete BIST data source here. Keeping this
    class separate lets the scoring and dashboard engine stay testable.
    """

    def fetch(self, ticker: str) -> FinancialStatements:
        raise NotImplementedError(
            "BIST provider is not connected yet. Use Colab integration or pass statements directly."
        )
