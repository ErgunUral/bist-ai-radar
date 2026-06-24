from __future__ import annotations

import argparse

from src.ai_decision import decision_from_score, risk_label
from src.scoring import calculate_score
from src.sector_rules import classify_ticker


def main() -> None:
    parser = argparse.ArgumentParser(description="BIST AI Radar CLI")
    parser.add_argument("ticker", help="BIST ticker symbol, e.g. ASELS")
    args = parser.parse_args()

    ticker = args.ticker.upper().strip()
    sector = classify_ticker(ticker)

    demo_metrics = {
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

    score = calculate_score(demo_metrics, sector).total_score

    print("BIST AI Radar V8")
    print("----------------")
    print(f"Hisse : {ticker}")
    print(f"Sektör: {sector}")
    print(f"Skor  : {score}")
    print(f"Karar : {decision_from_score(score)}")
    print(f"Risk  : {risk_label(score)}")
    print("\nNot: Bu CLI şu an demo metriklerle çalışır. Gerçek veri sağlayıcı entegrasyonu V8.1 aşamasındadır.")


if __name__ == "__main__":
    main()
