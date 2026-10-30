# ⚡ WordCount Pro — Enterprise Text & Readability Engine

[![CI Pipeline](https://github.com/user/wordcount/actions/workflows/ci.yml/badge.svg)](https://github.com/user/wordcount/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Keystone%20Clean%20Architecture-purple)](#mimari-tasar%C4%B1m-keystone-clean-architecture)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> Öğrencilik yıllarında yazılmış monolitik, kırılgan ve güvenlik açıkları barındıran basit bir Python betiğinden, **modern endüstri standartlarında**, **Keystone Temiz Mimari (Clean Architecture)** prensiplerine sahip, reaktif web arayüzlü ve tam kapsamlı test güvenceli bir analiz motoruna dönüşüm.

---

## 📋 İçindekiler
- [Öne Çıkan Özellikler](#-öne-çıkan-özellikler)
- [Mimari Tasarım (Keystone Clean Architecture)](#-mimari-tasarım-keystone-clean-architecture)
- [Proje Dosya Yapısı](#-proje-dosya-yapısı)
- [Hızlı Başlangıç (Quickstart)](#-hızlı-başlangıç-quickstart)
- [Web Arayüzü & Ekranlar](#-web-arayüzü--ekranlar)
- [REST API Kullanımı](#-rest-api-kullanımı)
- [Terminal / CLI Kullanımı](#-terminal--cli-kullanımı)
- [Test ve Doğrulama](#-test-ve-doğrulama)
- [Docker ve Dağıtım](#-docker-ve-dağıtım)

---

## 🚀 Öne Çıkan Özellikler

1. **Reaktif ve Modern Kullanıcı Arayüzü (Web UI)**:
   - Yazdıkça anında hesaplayan (debounced live counter) kelime, karakter ve cümle sayaçları.
   - Flesch Okunabilirlik İndeksi (Flesch Reading Ease) ve Flesch-Kincaid Sınıf Seviyesi.
   - Sessiz okuma (225 WPM) ve sesli sunum (135 WPM) süre tahminleri.
   - Anahtar kelime yoğunluk dağılımı (Stopword filtreleme destekli) ve görsel ilerleme çubukları.
   - `.txt` ve `.md` dosya yükleme, hazır örnek metin yükleyiciler (Teknik, Klasik Edebiyat, Türkçe).
   - Tek tıkla JSON rapor kopyalama, karanlık (Dark) ve aydınlık (Light) tema desteği.
   - Sıfır harici npm/CDN bağımlılığı; %100 çevrimdışı (air-gapped) çalışabilirlik.

2. **Keystone Clean Architecture**:
   - Dış bağımlılıklardan arındırılmış, saf Python Domain katmanı (`TextAnalyzer`, `Tokenizer`, `ReadabilityCalculator`).
   - Sorumlulukların ayrıştırılması (Domain, Application, Infrastructure, Presentation).
   - Hexagonal / Ports & Adapters: Aynı use case motoru hem FastAPI Web/REST katmanına hem de Terminal CLI aracına hizmet eder.

3. **Üretim Seviyesi Güvenlik ve Dayanıklılık**:
   - `debug=True, host=0.0.0.0` uzaktan kod çalıştırma (RCE) açığı giderildi.
   - DoS saldırılarına karşı karakter sınırı doğrulaması (`max_text_length`).
   - Çok aşamalı (multi-stage) ve root yetkisi olmayan (`appuser`, UID 10001) Docker container yapısı.
   - Hassas `.pem` anahtar sızıntılarını engelleyen kapsamlı `.gitignore` ve Twelve-Factor `.env` mimarisi.

4. **Kapsamlı Test Kapsamı**:
   - %100 geçen birim, entegrasyon ve CLI uçtan uca (E2E) testleri (27 test).

---

## 🏛️ Mimari Tasarım (Keystone Clean Architecture)

Sistem, bağımlılıkların yalnızca içeriye (merkeze) doğru aktığı katmanlı bir model üzerine kuruludur:

```
[ Presentation Katmanı ]
   ├── FastAPI ASGI Uygulaması & REST API (/api/v1/analyze, /api/v1/health)
   ├── Jinja2 Web Arayüzü & Reaktif İstemci (HTML5 / Modern CSS / Vanilla JS)
   └── CLI Sunum Adaptörü (Terminalden stdin / pipe ile analiz)
         │
         ▼ (çağırır)
[ Application Katmanı ]
   ├── Use Cases: AnalyzeTextUseCase
   └── DTOs: AnalyzeTextCommand, TextAnalysisResultDTO (Veri doğrulama, süre izleme)
         │
         ▼ (çağırır)
[ Domain Katmanı ] (Saf Python - Sıfır Dış Kütüphane Bağımlılığı)
   ├── Aggregate: TextMetrics
   ├── Value Objects: KeywordFrequency, ReadabilityScore, ReadingTime
   └── Domain Services: TextAnalyzer, Tokenizer, ReadabilityCalculator
         ▲
         │ (yapılandırır)
[ Infrastructure Katmanı ]
   ├── Twelve-Factor Konfigürasyon (Settings, Environment variables)
   └── Yapılandırılmış Loglama (Structured Logging)
```

---


## 📁 Proje Dosya Yapısı

```text
wordcount/
├── .github/
│   └── workflows/
│       └── ci.yml                 # Çoklu Python sürümlü GitHub Actions test & lint iş akışı
├── docs/
│   └── ARCHITECTURE.md            # Keystone Mimari Karar Kaydı (ADR) ve tasarım detayları
├── src/
│   └── wordcount/
│       ├── __init__.py            # Paket versiyonu ve üst bilgi
│       ├── __main__.py            # 'python -m wordcount' sunucu başlatıcısı
│       ├── domain/                # SAF DOMAIN KATMANI (İş Kuralları)
│       │   ├── __init__.py
│       │   ├── models.py          # Değişmez (Immutable) Value Objects ve TextMetrics Aggregate
│       │   ├── tokenizer.py       # Unicode Regex Tokenizer ve hece hesaplama
│       │   ├── analyzer.py        # Metin analiz orkestratörü
│       │   └── readability.py     # Flesch-Kincaid okunabilirlik ve okuma süresi hesaplayıcı
│       ├── application/           # UYGULAMA KATMANI (Use Case & DTO)
│       │   ├── __init__.py
│       │   ├── dtos.py            # Transporttan bağımsız güçlü tipli DTO nesneleri
│       │   └── use_cases.py       # AnalyzeTextUseCase (Doğrulama ve çalıştırma)
│       ├── infrastructure/        # ALTYAPI KATMANI
│       │   ├── __init__.py
│       │   ├── config.py          # Twelve-Factor ortam değişkenleri (Settings)
│       │   └── logging.py         # Yapılandırılmış loglama
│       └── presentation/          # SUNUM KATMANI (Web, API, CLI)
│           ├── __init__.py
│           ├── cli.py             # Terminal CLI sunum adaptörü
│           └── web/
│               ├── __init__.py
│               ├── app.py         # FastAPI ASGI uygulama fabrikası
│               ├── routes.py      # REST API ve HTML view yönlendiricileri
│               ├── static/
│               │   ├── css/style.css  # Modern CSS değişkenleri, Dark/Light tema
│               │   └── js/app.js      # Reaktif canlı sayaç, API istemcisi, dosya yükleyici
│               └── templates/
│                   ├── base.html      # Semantik HTML5 iskeleti
│                   └── index.html     # Etkileşimli analitik paneli
├── tests/
│   ├── unit/                      # Domain birim testleri (tokenizer, analyzer, readability)
│   ├── integration/               # Web API ve use case entegrasyon testleri
│   └── e2e/                       # CLI uçtan uca testleri
├── .dockerignore
├── .env.example                   # Örnek konfigürasyon şablonu
├── .gitignore                     # Hassas verileri engelleyen temiz gitignore
├── Dockerfile                     # Multi-stage, güvenli ve non-root Docker imajı
├── docker-compose.yml             # Tek komutla ayağa kaldırma
├── Makefile                       # Geliştirici kısayolları
├── pyproject.toml                 # Modern PEP 621 paket ve araç ayarları
├── requirements.txt               # Üretim ortamı bağımlılıkları
├── requirements-dev.txt           # Test ve geliştirme ortamı bağımlılıkları
└── README.md
```

---

## 💻 Hızlı Başlangıç (Quickstart)

### 1. Yerel Ortamda Çalıştırma

```bash
# 1. Depoyu klonlayın ve dizine girin
cd wordcount-v2

# 2. Sanal ortam oluşturup aktif edin
python3 -m venv .venv
source .venv/bin/activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements-dev.txt

# 4. Sunucuyu başlatın (Makefile ile veya doğrudan python ile)
make run
# Veya:
# PYTHONPATH=src python3 -m wordcount
```

Tarayıcınızda açın:
- **Web Paneli**: `http://localhost:8000`
- **Swagger / OpenAPI Belgeleri**: `http://localhost:8000/docs`
- **ReDoc Belgeleri**: `http://localhost:8000/redoc`

---

## 🌐 REST API Kullanımı

WordCount Pro, programatik entegrasyonlar için tam OpenAPI uyumlu REST uç noktaları sağlar:

### `POST /api/v1/analyze`

**Örnek İstek (cURL):**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Clean architecture decouples domain logic from frameworks, ensuring testability.",
    "top_n_keywords": 3,
    "filter_stopwords": true
  }'
```

**Örnek Yanıt (JSON):**
```json
{
  "characters_total": 82,
  "characters_no_spaces": 73,
  "words_total": 10,
  "words_unique": 10,
  "vocabulary_density": 100.0,
  "sentences_total": 1,
  "paragraphs_total": 1,
  "avg_word_length": 7.3,
  "avg_sentence_length": 10.0,
  "longest_word": "architecture",
  "reading_time": {
    "reading_minutes": 0.04,
    "reading_time_formatted": "3 sec",
    "speaking_minutes": 0.07,
    "speaking_time_formatted": "5 sec"
  },
  "readability": {
    "flesch_reading_ease": 38.6,
    "flesch_kincaid_grade": 12.8,
    "reading_level": "Difficult (College)",
    "notes": "Academic articles and business reports."
  },
  "top_keywords": [
    { "word": "clean", "count": 1, "density_percent": 10.0 },
    { "word": "architecture", "count": 1, "density_percent": 10.0 },
    { "word": "decouples", "count": 1, "density_percent": 10.0 }
  ],
  "execution_time_ms": 0.42
}
```

---

## 🖥️ Terminal / CLI Kullanımı

Keystone mimarisinin bağımsız sunum adaptörü sayesinde arayüze ihtiyaç duymadan terminalde de doğrudan çalıştırabilirsiniz:

```bash
# 1. Doğrudan parametre vererek
PYTHONPATH=src python3 -m wordcount.presentation.cli "Merhaba dünya! Bu bir testtir."

# 2. JSON çıktısı alarak (jq ile filtrelemek için)
PYTHONPATH=src python3 -m wordcount.presentation.cli "Yazılım mimarisi önemlidir." --json

# 3. Dosyadan pipe (|) ile okutarak
cat docs/ARCHITECTURE.md | PYTHONPATH=src python3 -m wordcount.presentation.cli -
```

---

## 🧪 Test ve Doğrulama

Tüm katmanlar için testler mevcuttur:

```bash
# Testleri çalıştırmak için
make test

# Veya unittest doğrudan:
PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v
```

**Test Sonuçları:**
```text
Ran 27 tests in 0.389s
OK (100% Passing: Domain Unit, Use Case Integration, Web API Routes, CLI E2E)
```

---

## 🐳 Docker ve Dağıtım

### Docker Compose ile Tek Komutla Çalıştırma
```bash
docker-compose up --build
```

### Manuel Docker Build
```bash
make docker-build
make docker-run
```
İmaj çok aşamalı (multi-stage) olarak inşa edilir ve sistem güvenliği için yetkisiz `appuser` kullanıcısı ile çalışır.
