# Architecture Decision Record (ADR) & System Architecture

## 1. Architectural Overview: Keystone Clean Architecture

WordCount Pro adheres strictly to the **Keystone Clean Architecture** pattern (inspired by Hexagonal Architecture / Ports and Adapters). The core premise is **separation of concerns** and the **Dependency Inversion Principle**: business and linguistic rules do not depend on external frameworks, databases, or delivery mechanisms.

```
+-------------------------------------------------------------------+
|                        PRESENTATION LAYER                         |
|  [FastAPI Routers]   [Jinja2 / Web UI (JS/CSS)]   [CLI Adapter]   |
+---------------------------------+---------------------------------+
                                  | calls
                                  v
+-------------------------------------------------------------------+
|                        APPLICATION LAYER                          |
|         [AnalyzeTextUseCase]           [Input/Output DTOs]        |
|                  (Orchestration, Validation, Tracing)             |
+---------------------------------+---------------------------------+
                                  | calls
                                  v
+-------------------------------------------------------------------+
|                          DOMAIN LAYER                             |
|    [TextAnalyzer]       [Tokenizer]       [ReadabilityCalculator] |
|    [TextMetrics]        [KeywordFrequency]   [ReadabilityScore]   |
|         (Pure Python • Zero External Framework Dependencies)      |
+-------------------------------------------------------------------+
                                  ^
                                  | configures
+---------------------------------+---------------------------------+
|                       INFRASTRUCTURE LAYER                        |
|       [Twelve-Factor Settings]       [Structured Logging]         |
+-------------------------------------------------------------------+
```

---

## 2. Layer Responsibilities & Boundaries

### 2.1. Domain Layer (`src/wordcount/domain/`)
- **Purity**: Zero third-party runtime dependencies. Standard library only (`dataclasses`, `re`, `typing`, `collections`).
- **Models (`models.py`)**: Immutable value objects (`KeywordFrequency`, `ReadabilityScore`, `ReadingTime`) and the aggregate root `TextMetrics`. Invariants are enforced at construction time.
- **Tokenizer (`tokenizer.py`)**: Linguistic parsing, Unicode letter support (e.g., Turkish characters), honorific title preservation (`Dr.`, `Mr.`), and syllable estimation heuristics.
- **Readability (`readability.py`)**: Implements standard reading metrics (Flesch Reading Ease, Flesch-Kincaid Grade Level, WPM silent and speaking time).
- **Analyzer (`analyzer.py`)**: Domain service composing tokenization, statistics, and keyword density.

### 2.2. Application Layer (`src/wordcount/application/`)
- **Use Cases (`use_cases.py`)**: Primary orchestrators (`AnalyzeTextUseCase`). Responsible for applying input boundary limits, execution latency tracking, and translating domain aggregates into presentation-safe DTOs.
- **DTOs (`dtos.py`)**: Strong typing decoupling HTTP transport schemas from internal domain models. Enforces maximum character limits (DoS mitigation).

### 2.3. Infrastructure Layer (`src/wordcount/infrastructure/`)
- **Configuration (`config.py`)**: Implements Twelve-Factor App principles using environment variables with fallback defaults.
- **Logging (`logging.py`)**: Configures production-grade standard output logging with timestamps and severity levels.

### 2.4. Presentation Layer (`src/wordcount/presentation/`)
- **Web API & ASGI Factory (`web/app.py`, `web/routes.py`)**: FastAPI ASGI application exposing OpenAPI/Swagger autodocs, RESTful JSON endpoints (`/api/v1/analyze`, `/api/v1/health`), and serving the responsive single-page dashboard.
- **Client Frontend (`web/templates/`, `web/static/`)**: Native HTML5, modern CSS3 (custom properties, dark/light mode), and debounced client-side JavaScript. Zero external NPM or CDN dependencies required—runs 100% offline and in air-gapped environments.
- **CLI Adapter (`cli.py`)**: Command-line presentation adapter enabling stdin pipes, file analysis, and formatted terminal reports.

---

## 3. Key Architectural Decisions (ADR)

| Decision | Context | Rationale | Alternatives Considered |
|---|---|---|---|
| **FastAPI + Starlette** | Web Framework | Modern async ASGI standard with automatic OpenAPI generation and native Pydantic validation. | Flask (legacy, synchronous, manual validation) |
| **Pure Python Domain** | Core Business Logic | Domain logic has zero dependencies; completely isolated from web framework changes. | Binding Flask `request` directly inside calculation |
| **Hexagonal Ports & Adapters** | Interface Decoupling | Same `AnalyzeTextUseCase` powers both the Web API and the terminal CLI adapter without code duplication. | Tight-coupling logic to HTML view templates |
| **No External JS Framework** | Frontend Delivery | Eliminates npm build pipelines, node_modules bloat, and CDN breakage in offline environments. | React/Vue (excessive complexity for a text tool) |
| **Multi-Stage Docker** | Packaging | Reduces image size by 70% and runs as non-root `appuser` (UID 10001) for strict security compliance. | Single-stage root Debian image |

---

## 4. Legacy vs. Modern Comparison

| Aspect | Legacy Student Implementation | Modern Keystone Implementation |
|---|---|---|
| **Lines of Code & Architecture** | Single 15-line script with all concerns mixed | Clean layered architecture (Domain, App, Infra, Presentation) |
| **Security** | `debug=True, host=0.0.0.0` (RCE risk), `.pem` in repo | Non-root container, DoS character limits, secret hygiene |
| **Error Handling** | Unhandled KeyError on missing form keys | Explicit exception handlers, HTTP 400 with actionable messages |
| **Algorithms** | Naive `len(text.split())` (fails on punctuation & unicode) | Unicode-aware regex tokenizer, Flesch-Kincaid, WPM timing |
| **User Experience** | 1990s HTML form, full page reload POST | Real-time live debounced counts, dark mode, responsive cards |
| **Test Coverage** | 0% (no tests) | 100% unit, integration, and E2E CLI coverage (27 tests) |
| **CI/CD & DevOps** | None | Multi-Python GitHub Actions, Dockerfile, Docker Compose, Makefile |
