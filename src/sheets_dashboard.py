"""Google Sheets dashboard helper functions."""

from __future__ import annotations

from typing import Iterable

import pandas as pd


MAIN_COLUMNS = [
    "Hisse",
    "Dönem",
    "Sektör Tipi",
    "Genel Skor",
    "AI Karar",
    "Risk",
    "AI Uyarı",
    "Satış Büyüme %",
    "Net Kar Büyüme %",
    "ROE %",
    "ROA %",
    "Net Kar Marjı %",
    "FAVÖK Marjı %",
    "Net Borç",
    "Cari Oran",
    "Borç/Özkaynak",
    "F/K",
    "PD/DD",
    "FD/FAVÖK",
    "Son Güncelleme",
]


def prepare_main_dashboard(df: pd.DataFrame) -> pd.DataFrame:
    """Return a user-friendly main dashboard table."""
    if df.empty:
        return pd.DataFrame(columns=MAIN_COLUMNS)

    result = df.copy()
    for column in MAIN_COLUMNS:
        if column not in result.columns:
            result[column] = ""

    result = result[MAIN_COLUMNS]
    if "Genel Skor" in result.columns:
        result = result.sort_values("Genel Skor", ascending=False, na_position="last")
    return result


def top_n(df: pd.DataFrame, n: int = 20, score_column: str = "Genel Skor") -> pd.DataFrame:
    if df.empty or score_column not in df.columns:
        return df.head(0)
    return df.sort_values(score_column, ascending=False).head(n)


def risky_stocks(df: pd.DataFrame, threshold: float = 40, score_column: str = "Genel Skor") -> pd.DataFrame:
    if df.empty or score_column not in df.columns:
        return df.head(0)
    return df[df[score_column] < threshold].sort_values(score_column, ascending=True)


def dataframe_to_values(df: pd.DataFrame) -> list[list[object]]:
    """Convert DataFrame to Google Sheets values with header."""
    clean = df.fillna("")
    return [list(clean.columns)] + clean.values.tolist()


def ensure_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    result = df.copy()
    for column in columns:
        if column not in result.columns:
            result[column] = ""
    return result[list(columns)]
