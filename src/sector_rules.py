"""Sector classification and score profile definitions."""

from __future__ import annotations

from enum import StrEnum


class SectorType(StrEnum):
    INDUSTRIAL = "Sanayi"
    BANK = "Banka"
    REIT = "GYO"
    HOLDING = "Holding"
    INSURANCE = "Sigorta"
    FINANCIAL = "Finansal"
    UNKNOWN = "Bilinmiyor"


BANK_TICKERS = {
    "AKBNK", "GARAN", "HALKB", "ISCTR", "YKBNK", "VAKBN", "TSKB", "SKBNK", "ALBRK",
}

REIT_SUFFIXES = ("GYO",)
HOLDING_SUFFIXES = ("HOL",)
INSURANCE_TICKERS = {"AKGRT", "ANSGR", "TURSG"}


def classify_ticker(ticker: str) -> SectorType:
    symbol = ticker.upper().replace(".IS", "").strip()
    if symbol in BANK_TICKERS:
        return SectorType.BANK
    if symbol.endswith(REIT_SUFFIXES):
        return SectorType.REIT
    if symbol.endswith(HOLDING_SUFFIXES):
        return SectorType.HOLDING
    if symbol in INSURANCE_TICKERS:
        return SectorType.INSURANCE
    return SectorType.INDUSTRIAL


SCORE_WEIGHTS = {
    SectorType.INDUSTRIAL: {
        "financial_health": 25,
        "profitability": 25,
        "growth": 20,
        "cash_flow": 15,
        "leverage": 10,
        "valuation": 5,
    },
    SectorType.BANK: {
        "financial_health": 20,
        "profitability": 35,
        "growth": 20,
        "cash_flow": 0,
        "leverage": 10,
        "valuation": 15,
    },
    SectorType.REIT: {
        "financial_health": 30,
        "profitability": 20,
        "growth": 15,
        "cash_flow": 10,
        "leverage": 15,
        "valuation": 10,
    },
    SectorType.HOLDING: {
        "financial_health": 25,
        "profitability": 20,
        "growth": 15,
        "cash_flow": 10,
        "leverage": 15,
        "valuation": 15,
    },
}


def get_score_weights(sector_type: SectorType) -> dict[str, int]:
    return SCORE_WEIGHTS.get(sector_type, SCORE_WEIGHTS[SectorType.INDUSTRIAL])
