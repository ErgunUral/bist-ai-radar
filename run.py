from __future__ import annotations

import argparse
import sys

from src.analyzer import analyze_statements
from src.bist_provider import BistProvider
from src.formatter import format_analysis_result
from src.sample_data import build_sample_statements


def run_demo(ticker: str) -> None:
    result = analyze_statements(
        ticker=ticker,
        statements=build_sample_statements(),
        market_value=1000,
    )
    print(format_analysis_result(result))
    print("\nNot: Demo modunda örnek finansal tablolarla çalışır. Gerçek veri için --provider kullanılır.")


def run_provider(ticker: str) -> None:
    provider = BistProvider()
    try:
        statements = provider.fetch(ticker)
        result = analyze_statements(ticker=ticker, statements=statements)
        print(format_analysis_result(result))
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
    parser.add_argument("--provider", action="store_true", help="Use real data provider instead of demo statements")
    args = parser.parse_args()

    ticker = args.ticker.upper().strip()
    if args.provider:
        run_provider(ticker)
    else:
        run_demo(ticker)


if __name__ == "__main__":
    main()
