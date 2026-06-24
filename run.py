from __future__ import annotations

import argparse
import sys

from src.ai_decision import build_warnings, decision_from_score, risk_label
from src.bist_provider import BistProvider
from src.scoring import calculate_score
from src.sector_rules import classify_ticker


DEMO_METRICS = {
    "current_ratio": 2.0,
    "debt_to_equity": 0.8,
    "net_debt": -1.0,
    "roe": 22.0,
    "roa": 9.0,
    "net_margin": 12.0,
    "ebitda_margin": 18.0,
    "revenue_growth": 10.0,
    "net_income_growth": 15.0,
    "free_cash_flow": 1.0,
    "price_to_earnings": 12.0,
    "price_to_book": 1.5,
}


def print_result(ticker: str, sector: object, score: float, metrics: dict, mode: str) -> None:
    print("BIST AI Radar V8.1")
    print("------------------")
    print(f"Mod   : {mode}")
    print(f"Hisse : {ticker}")
    print(f"Sektör: {sector}")
    print(f"Skor  : {score}")
    print(f"Karar : {decision_from_score(score)}")
    print(f"Risk  : {risk_label(score)}")
    print(f"Uyarı : {build_warnings(metrics)}")


def run_demo(ticker: str) -> None:
    sector = classify_ticker(ticker)
    score = calculate_score(DEMO_METRICS, sector).total_score
    print_result(ticker, sector, score, DEMO_METRICS, "Demo")
    print("\nNot: Demo modunda örnek metriklerle çalışır. Gerçek veri için --provider kullanılır.")


def run_provider(ticker: str) -> None:
    provider = BistProvider()
    try:
        provider.fetch(ticker)
    except NotImplementedError as exc:
        print("BIST AI Radar V8.1")
        print("------------------")
        print(f"Hisse : {ticker}")
        print("Durum : Gerçek BIST provider henüz bağlı değil")
        print(f"Detay : {exc}")
        sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="BIST AI Radar CLI")
    parser.add_argument("ticker", help="BIST ticker symbol, e.g. ASELS")
    parser.add_argument("--provider", action="store_true", help="Use real data provider instead of demo metrics")
    args = parser.parse_args()

    ticker = args.ticker.upper().strip()
    if args.provider:
        run_provider(ticker)
    else:
        run_demo(ticker)


if __name__ == "__main__":
    main()
