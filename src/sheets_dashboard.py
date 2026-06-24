"""Google Sheets dashboard helper functions."""

from __future__ import annotations

from datetime import datetime
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


def get_or_create_worksheet(spreadsheet, title: str, rows: int = 1000, cols: int = 30):
    """Get worksheet by title or create it if missing."""
    try:
        return spreadsheet.worksheet(title)
    except Exception:
        return spreadsheet.add_worksheet(title=title, rows=rows, cols=cols)


def backup_worksheet(spreadsheet, worksheet, prefix: str = "Yedek") -> str:
    """Copy existing worksheet before destructive updates."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_title = f"{prefix}_{worksheet.title}_{timestamp}"
    try:
        worksheet.duplicate(new_sheet_name=backup_title)
    except Exception:
        backup_ws = spreadsheet.add_worksheet(title=backup_title, rows=worksheet.row_count, cols=worksheet.col_count)
        values = worksheet.get_all_values()
        if values:
            backup_ws.update(values=values, range_name="A1")
    return backup_title


def safe_update_worksheet(spreadsheet, worksheet_name: str, df: pd.DataFrame, *, backup: bool = True):
    """Safely update a worksheet.

    This function never clears a sheet when the dataframe is empty. It also
    creates a backup copy before replacing data by default.
    """
    if df is None or df.empty:
        raise ValueError("Dashboard boş geldi. Sayfa temizlenmedi; veri kaybı engellendi.")

    worksheet = get_or_create_worksheet(spreadsheet, worksheet_name)
    backup_title = backup_worksheet(spreadsheet, worksheet) if backup else None

    values = dataframe_to_values(df)
    worksheet.clear()
    worksheet.update(values=values, range_name="A1")

    try:
        worksheet.freeze(rows=1)
        worksheet.format("A1:Z1", {
            "textFormat": {"bold": True},
            "horizontalAlignment": "CENTER",
        })
    except Exception:
        pass

    return {"worksheet": worksheet.title, "backup": backup_title, "rows": len(df)}
