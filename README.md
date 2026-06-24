# BIST AI Radar

BIST AI Radar; BIST şirketleri için temel analiz, dönem kontrolü, finansal oran hesaplama, skor üretimi ve Google Sheets dashboard çıktısı hazırlamak için geliştirilmiş Python tabanlı analiz projesidir.

## Hedef

- En güncel açıklanan finansal dönemi otomatik seçmek
- Bilanço, gelir tablosu ve nakit akış verilerini eşleştirmek
- Sektöre göre doğru oranları hesaplamak
- 0-100 arası temel skor üretmek
- AI karar ve uyarı kolonları oluşturmak
- Google Sheets üzerinde sade ve kullanıcı dostu dashboard üretmek

## Colab

Colab notebook:

```text
notebooks/BIST_AI_Radar_V8_Colab.ipynb
```

GitHub üzerinden açıp **Open in Colab** ile çalıştırılabilir.

## Lokal Kullanım

```bash
git clone https://github.com/ErgunUral/bist-ai-radar.git
cd bist-ai-radar
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
python run.py ASELS
```

Gerçek provider denemesi:

```bash
python run.py ASELS --provider
```

## Klasör Yapısı

```text
bist-ai-radar
├── notebooks
│   ├── BIST_AI_Radar_V8.ipynb
│   └── BIST_AI_Radar_V8_Colab.ipynb
├── src
│   ├── analyzer.py
│   ├── bist_provider.py
│   ├── data_fetcher.py
│   ├── financial_mapper.py
│   ├── formatter.py
│   ├── period_manager.py
│   ├── ratios.py
│   ├── sample_data.py
│   ├── scoring.py
│   ├── sector_rules.py
│   ├── ai_decision.py
│   └── sheets_dashboard.py
├── tests
├── docs
├── run.py
├── pyproject.toml
└── requirements.txt
```

## Durum

V8.1 çekirdek motor, CLI demo modu, testler ve Colab demo akışı hazırdır. Gerçek BIST veri sağlayıcı entegrasyonu için `src/bist_provider.py` içindeki `BistProvider.fetch()` fonksiyonu canlı veri kaynağına bağlanmalıdır.

## Yasal Uyarı

Bu proje yatırım tavsiyesi değildir. Üretilen skorlar ve karar etiketleri yalnızca analitik değerlendirme amaçlıdır.
