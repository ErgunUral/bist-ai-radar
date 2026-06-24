"""Financial period parsing and selection utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class FinancialPeriod:
    """Comparable financial period such as Q3/2026."""

    year: int
    quarter: int
    raw: str

    @property
    def label(self) -> str:
        return f"Q{self.quarter}/{self.year}"


_PERIOD_PATTERNS = [
    re.compile(r"Q\s*([1-4])\s*[/\-]\s*(20\d{2})", re.IGNORECASE),
    re.compile(r"(20\d{2})\s*[/\-]\s*Q\s*([1-4])", re.IGNORECASE),
    re.compile(r"(20\d{2})\s*[/\-]\s*([1-4])"),
]


def parse_period(value: object) -> FinancialPeriod | None:
    """Parse common BIST period labels into a comparable object."""
    text = str(value).strip()
    if not text:
        return None

    for pattern in _PERIOD_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue

        groups = match.groups()
        if groups[0].startswith("20"):
            year = int(groups[0])
            quarter = int(groups[1])
        else:
            quarter = int(groups[0])
            year = int(groups[1])
        return FinancialPeriod(year=year, quarter=quarter, raw=text)

    return None


def sort_periods(periods: list[object], descending: bool = True) -> list[str]:
    """Sort detected financial periods by year and quarter."""
    parsed = [p for p in (parse_period(item) for item in periods) if p is not None]
    return [p.raw for p in sorted(parsed, reverse=descending)]


def latest_period(periods: list[object]) -> str | None:
    """Return the latest available period label."""
    sorted_periods = sort_periods(periods, descending=True)
    return sorted_periods[0] if sorted_periods else None


def select_recent_periods(periods: list[object], limit: int = 4) -> list[str]:
    """Return latest N available periods."""
    return sort_periods(periods, descending=True)[:limit]
