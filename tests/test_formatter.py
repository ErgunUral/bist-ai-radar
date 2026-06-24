from src.analyzer import analyze_statements
from src.formatter import format_analysis_result
from src.sample_data import build_sample_statements


def test_formatter_contains_key_sections():
    result = analyze_statements("ASELS", build_sample_statements(), market_value=1000)
    text = format_analysis_result(result)

    assert "BIST AI Radar V8.1" in text
    assert "Hisse : ASELS" in text
    assert "Öne Çıkan Oranlar" in text
    assert "Uyarı:" in text
