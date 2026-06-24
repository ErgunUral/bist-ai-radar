from __future__ import annotations


def fmt_number(value: object, digits: int = 2) -> str:
    if value is None or value == "":
        return "-"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{number:,.{digits}f}"


def fmt_percent(value: object, digits: int = 2) -> str:
    if value is None or value == "":
        return "-"
    try:
        return f"{float(value):,.{digits}f}%"
    except (TypeError, ValueError):
        return str(value)


def format_analysis_result(result) -> str:
    data = result.to_dict()
    lines = [
        "BIST AI Radar V8.1",
        "------------------",
        f"Hisse : {data.get('ticker', '-')}",
        f"Dönem : {data.get('period', '-')}",
        f"Sektör: {data.get('sector_type', '-')}",
        f"Skor  : {fmt_number(data.get('total_score'))}",
        f"Karar : {data.get('decision', '-')}",
        f"Risk  : {data.get('risk', '-')}",
        "",
        "Öne Çıkan Oranlar",
        f"ROE          : {fmt_percent(data.get('roe'))}",
        f"ROA          : {fmt_percent(data.get('roa'))}",
        f"Net Marj     : {fmt_percent(data.get('net_margin'))}",
        f"FAVÖK Marjı  : {fmt_percent(data.get('ebitda_margin'))}",
        f"Cari Oran    : {fmt_number(data.get('current_ratio'))}",
        f"Borç/Özkaynak: {fmt_number(data.get('debt_to_equity'))}",
        f"F/K          : {fmt_number(data.get('price_to_earnings'))}",
        f"PD/DD        : {fmt_number(data.get('price_to_book'))}",
        "",
        f"Uyarı: {data.get('warnings', '-')}",
    ]
    return "\n".join(lines)
