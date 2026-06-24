# BIST AI Radar

BIST AI Radar; BIST şirketleri için temel analiz, dönem kontrolü, finansal oran hesaplama, skor üretimi ve Google Sheets dashboard çıktısı hazırlamak için geliştirilmiş Python tabanlı analiz projesidir.

## Hedef

- En güncel açıklanan finansal dönemi otomatik seçmek
- Bilanço, gelir tablosu ve nakit akış verilerini eşleştirmek
- Sektöre göre doğru oranları hesaplamak
- 0-100 arası temel skor üretmek
- AI karar ve uyarı kolonları oluşturmak
- Google Sheets üzerinde sade ve kullanıcı dostu dashboard üretmek

## Klasör Yapısı

```text
bist-ai-radar
├── notebooks
│   └── BIST_AI_Radar_V8.ipynb
├── src
│   ├── data_fetcher.py
│   ├── period_manager.py
│   ├── financial_mapper.py
│   ├── ratios.py
│   ├── sector_rules.py
│   ├── scoring.py
│   ├── ai_decision.py
│   └── sheets_dashboard.py
├── tests
│   ├── test_period.py
│   ├── test_ratios.py
│   └── test_scoring.py
├── docs
│   └── scoring.md
└── requirements.txt
```

## Durum

V8 geliştirmesi başladı. İlk aşamada kod modüler hale getiriliyor.

## Yasal Uyarı

Bu proje yatırım tavsiyesi değildir. Üretilen skorlar ve karar etiketleri yalnızca analitik değerlendirme amaçlıdır.
