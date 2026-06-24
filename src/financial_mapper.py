"""Financial statement row mapping helpers."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd


FIELD_ALIASES: dict[str, list[str]] = {
    "cash": [
        "nakit ve nakit benzerleri",
        "nakit ve nakit benzeri",
        "hazır değerler",
        "cash and cash equivalents",
        "nakit",
    ],
    "financial_investments": [
        "finansal yatırımlar",
        "kısa vadeli finansal yatırımlar",
        "financial investments",
    ],
    "current_assets": [
        "dönen varlıklar",
        "toplam dönen varlıklar",
        "current assets",
    ],
    "current_liabilities": [
        "kısa vadeli yükümlülükler",
        "toplam kısa vadeli yükümlülükler",
        "current liabilities",
    ],
    "total_assets": [
        "toplam varlıklar",
        "varlıklar toplamı",
        "total assets",
    ],
    "total_liabilities": [
        "toplam yükümlülükler",
        "yükümlülükler toplamı",
        "total liabilities",
    ],
    "equity": [
        "ana ortaklığa ait özkaynaklar",
        "toplam özkaynaklar",
        "özkaynaklar",
        "equity",
    ],
    "short_financial_debt": [
        "kısa vadeli borçlanmalar",
        "kısa vadeli finansal borçlar",
        "short term borrowings",
    ],
    "long_financial_debt": [
        "uzun vadeli borçlanmalar",
        "uzun vadeli finansal borçlar",
        "long term borrowings",
    ],
    "revenue": [
        "hasılat",
        "satış gelirleri",
        "net satışlar",
        "revenue",
        "sales",
    ],
    "gross_profit": [
        "brüt kar",
        "brüt kâr",
        "gross profit",
    ],
    "operating_profit": [
        "esas faaliyet karı",
        "esas faaliyet kârı",
        "faaliyet karı",
        "operating profit",
    ],
    "ebitda": [
        "favök",
        "ebitda",
    ],
    "net_income": [
        "ana ortaklık payları net dönem karı",
        "ana ortaklık net dönem karı",
        "net dönem karı",
        "dönem karı",
        "net income",
    ],
    "operating_cash_flow": [
        "işletme faaliyetlerinden nakit akışları",
        "faaliyetlerden sağlanan nakit akışı",
        "operating cash flow",
    ],
    "capex": [
        "maddi duran varlık alımları",
        "yatırım harcamaları",
        "capex",
    ],
}


def normalize_text(value: object) -> str:
    text = str(value).lower().strip()
    replacements = str.maketrans({"ı": "i", "İ": "i", "ğ": "g", "ü": "u", "ş": "s", "ö": "o", "ç": "c"})
    text = text.translate(replacements)
    text = re.sub(r"\s+", " ", text)
    return text


def find_row_label(index_values: Iterable[object], aliases: list[str]) -> object | None:
    normalized_aliases = [normalize_text(alias) for alias in aliases]
    rows = list(index_values)

    for row in rows:
        normalized_row = normalize_text(row)
        if normalized_row in normalized_aliases:
            return row

    for row in rows:
        normalized_row = normalize_text(row)
        if any(alias in normalized_row for alias in normalized_aliases):
            return row

    return None


def get_value(statement: pd.DataFrame | None, field: str, period: str | None = None, default: float = 0.0) -> float:
    """Return a numeric financial value by semantic field alias."""
    if statement is None or statement.empty or field not in FIELD_ALIASES:
        return default

    row = find_row_label(statement.index, FIELD_ALIASES[field])
    if row is None:
        return default

    column = period if period in statement.columns else statement.columns[0]
    value = statement.loc[row, column]

    try:
        return float(str(value).replace(".", "").replace(",", "."))
    except (TypeError, ValueError):
        return default


def available_fields(statement: pd.DataFrame | None) -> list[str]:
    if statement is None or statement.empty:
        return []
    found: list[str] = []
    for field, aliases in FIELD_ALIASES.items():
        if find_row_label(statement.index, aliases) is not None:
            found.append(field)
    return found
