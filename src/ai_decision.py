"""Decision labels and warning generation for BIST AI Radar."""

from __future__ import annotations


def decision_from_score(score: float) -> str:
    if score >= 85:
        return "🟢 Güçlü AL"
    if score >= 70:
        return "🟢 AL"
    if score >= 55:
        return "🟡 TUT"
    if score >= 40:
        return "🟠 İZLE"
    return "🔴 RİSK"


def risk_label(score: float) -> str:
    if score >= 75:
        return "Düşük"
    if score >= 55:
        return "Orta"
    if score >= 40:
        return "Yüksek"
    return "Çok Yüksek"


def build_warnings(row: dict) -> str:
    warnings: list[str] = []

    net_income_growth = row.get("net_income_growth")
    roe = row.get("roe")
    net_margin = row.get("net_margin")
    debt_to_equity = row.get("debt_to_equity")
    current_ratio = row.get("current_ratio")
    free_cash_flow = row.get("free_cash_flow")

    if net_income_growth is not None and net_income_growth < 0:
        warnings.append("⚠️ Net kâr düşüyor")
    if roe is not None and roe >= 20:
        warnings.append("✅ ROE güçlü")
    if net_margin is not None and net_margin < 0:
        warnings.append("⚠️ Net marj negatif")
    if debt_to_equity is not None and debt_to_equity > 2:
        warnings.append("⚠️ Borç yüksek")
    if current_ratio is not None and current_ratio < 1:
        warnings.append("⚠️ Cari oran zayıf")
    if free_cash_flow is not None and free_cash_flow < 0:
        warnings.append("⚠️ Serbest nakit akışı negatif")

    return " | ".join(warnings) if warnings else "✅ Belirgin uyarı yok"
