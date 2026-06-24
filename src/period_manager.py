"""Financial period parsing and locked period selection utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True, order=True)
class FinancialPeriod:
    """Comparable financial period such as Q3/2026."""

    year: int
    quarter: int
    raw: str

    @property
    def key(self) -> tuple[int, int]:
        return (self.year, self.quarter)

    @property
    def label(self) -> str:
        return f"Q{self.quarter}/{self.year}"


def period_key_from_value(value: object) -> tuple[int, int]:
    """Convert many BIST period representations into a stable (year, quarter) key."""
    if value is None:
        return (0, 0)

    try:
        dt = pd.to_datetime(value, errors="coerce", dayfirst=True)
        if pd.notna(dt) and not isinstance(value, str):
            quarter = 1 if dt.month <= 3 else 2 if dt.month <= 6 else 3 if dt.month <= 9 else 4
            return (int(dt.year), quarter)
    except Exception:
        pass

    text = str(value).strip()
    if not text:
        return (0, 0)

    normalized = text.replace("Ç", "C").replace("ç", "c")

    patterns = [
        (r"Q\s*([1-4])\s*[-_/ ]?\s*(20\d{2})", "q_year"),
        (r"([1-4])\s*Q\s*[-_/ ]?\s*(20\d{2})", "q_year"),
        (r"(20\d{2})\s*[-_/ ]?\s*Q\s*([1-4])", "year_q"),
        (r"(20\d{2})\s*[-_/ ]?\s*([1-4])\s*Q", "year_q"),
    ]
    for pattern, kind in patterns:
        match = re.search(pattern, normalized, re.IGNORECASE)
        if not match:
            continue
        if kind == "q_year":
            return (int(match.group(2)), int(match.group(1)))
        return (int(match.group(1)), int(match.group(2)))

    match = re.search(r"(20\d{2})[-_/\.](\d{1,2})(?:[-_/\.](\d{1,2}))?", normalized)
    if match:
        year, month = int(match.group(1)), int(match.group(2))
        if 1 <= month <= 12:
            quarter = 1 if month <= 3 else 2 if month <= 6 else 3 if month <= 9 else 4
            return (year, quarter)

    match = re.search(r"(\d{1,2})[-_/\.](\d{1,2})[-_/\.](20\d{2})", normalized)
    if match:
        month, year = int(match.group(2)), int(match.group(3))
        if 1 <= month <= 12:
            quarter = 1 if month <= 3 else 2 if month <= 6 else 3 if month <= 9 else 4
            return (year, quarter)

    match = re.search(r"^(20\d{2})(\d{2})$", normalized)
    if match:
        year, month = int(match.group(1)), int(match.group(2))
        if 1 <= month <= 12:
            quarter = 1 if month <= 3 else 2 if month <= 6 else 3 if month <= 9 else 4
            return (year, quarter)

    match = re.search(r"(20\d{2}).*?([1-4]).*?(ceyrek|quarter)", normalized, re.IGNORECASE)
    if match:
        return (int(match.group(1)), int(match.group(2)))

    try:
        dt = pd.to_datetime(text, errors="coerce", dayfirst=True)
        if pd.notna(dt):
            quarter = 1 if dt.month <= 3 else 2 if dt.month <= 6 else 3 if dt.month <= 9 else 4
            return (int(dt.year), quarter)
    except Exception:
        pass

    return (0, 0)


def parse_period(value: object) -> FinancialPeriod | None:
    """Parse common BIST period labels into a comparable object."""
    year, quarter = period_key_from_value(value)
    if not year or not quarter:
        return None
    return FinancialPeriod(year=year, quarter=quarter, raw=str(value).strip())


def period_label_from_key(key: tuple[int, int]) -> str:
    year, quarter = key
    return f"Q{quarter}/{year}" if year and quarter else ""


def sort_periods(periods: list[object], descending: bool = True) -> list[str]:
    parsed = [p for p in (parse_period(item) for item in periods) if p is not None]
    return [p.raw for p in sorted(parsed, reverse=descending)]


def latest_period(periods: list[object]) -> str | None:
    sorted_periods = sort_periods(periods, descending=True)
    return sorted_periods[0] if sorted_periods else None


def select_recent_periods(periods: list[object], limit: int = 4) -> list[str]:
    return sort_periods(periods, descending=True)[:limit]


def valid_columns(df) -> list[object]:
    if df is None or getattr(df, "empty", True):
        return []
    return [column for column in df.columns if df[column].notna().any()]


def period_keys_from_frame(df) -> list[tuple[int, int]]:
    keys = []
    for column in valid_columns(df):
        key = period_key_from_value(column)
        if key != (0, 0):
            keys.append(key)
    return keys


def period_keys_from_tables(*frames, limit: int = 4) -> list[tuple[int, int]]:
    keys: set[tuple[int, int]] = set()
    for frame in frames:
        keys.update(period_keys_from_frame(frame))
    return sorted(keys, reverse=True)[:limit]


def find_column_by_period(df, period_key: tuple[int, int]):
    if df is None or getattr(df, "empty", True):
        return None
    for column in valid_columns(df):
        if period_key_from_value(column) == period_key:
            return column
    return None


def select_period_keys(frames: Iterable, target_periods: list[object] | None = None, limit: int = 4) -> list[tuple[int, int]]:
    available = period_keys_from_tables(*frames, limit=999)
    if target_periods:
        wanted = {period_key_from_value(item) for item in target_periods}
        selected = [key for key in available if key in wanted and key != (0, 0)]
        if selected:
            return selected[:limit]
    return available[:limit]
