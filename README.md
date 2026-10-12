# Crawling and Automation

A collection of Python web-automation experiments, modernized into a small reusable package. The original 2020-2022 exercises are kept in `legacy/` for reproducibility and historical reference. The maintained code is in `src/crawling_automation/`.

> **Historical project notice:** Live third-party websites and the Meta Graph API have changed since the original exercises. The new Bama parser describes the archived HTML format and **is not verified against today's website**. Instagram metric availability depends on the API version, account permissions and access tokens. Collect only data you are authorized to access and respect target-site policies and rate limits.

## Features

- Deterministic vehicle price utilities: rounding, inspection-price bands, damage factors and mileage adjustments.
- Bama historic-format price-list parser, with a configurable HTTP client, timeout and CSV output.
- Read-only Instagram Business/Creator Graph API client with account discovery, paginated post listing and caller-selected insights.
- Offline regression tests that never require a live external account.

Unlike the historical Bama exercise, the maintained parser does **not** add randomness to recorded prices.

## Setup

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -e '.[dev]'
python -m unittest discover -s tests -v
```

## Run

```bash
# Attempt extraction from a compatible Bama price-list HTML structure.
crawl-auto bama --output .local/bama.csv --url https://bama.ir/price

# Instagram access requires a supported version and a valid account token.
export META_ACCESS_TOKEN='your_token_here'
export META_GRAPH_API_VERSION='vXX.X'  # Replace with a supported version.
crawl-auto instagram-posts --account-id YOUR_IG_ACCOUNT_ID --output .local/posts.csv
crawl-auto instagram-insights --account-id YOUR_IG_ACCOUNT_ID \\
  --metrics reach --since 2026-10-01 --until 2026-10-08 \\
  --output .local/insights.csv
```

The `--account-id` option is optional if the token can discover a linked Instagram account through `/me/accounts`. The insight metric names are explicit because supported metrics and permissions change. Consult official Meta documentation for the selected API version before attempting a live request. The maintained clients perform no network calls when imported.

For Bama, `--brand-map brands.json` accepts an optional JSON object mapping Persian brand names to English names. If omitted, the English brand column is blank rather than guessed. The recorded price remains in tomans and is never randomly adjusted.

### Python API

```python
from crawling_automation.automotive.pricing import (
    MileageRule, damage_adjusted_price, mileage_adjusted_price,
)

price = damage_adjusted_price(100_000_000, [1], {1: 0.975})
rules = {1397: MileageRule(1.055, 500, 20000, 60000, 0.9193)}
adjusted = mileage_adjusted_price(1397, price, 30000, rules)
```

The legacy dollar-delimited damage factors can be loaded with `load_damage_coefficients(stream)`. Mileage rules are injected; the original historical rule table remains in `legacy/automotive/Kilometr/kilometr.py` and has not been independently validated for contemporary pricing.

## Repository layout

| Directory | Purpose |
| --- | --- |
| `src/crawling_automation/automotive/` | Tested price calculations and HTML parsing |
| `src/crawling_automation/social/` | Configurable Meta Graph API adapter |
| `tests/` | Offline unit tests with fake HTTP sessions |
| `docs/` | Architecture, scope, privacy and migration notes |
| `legacy/automotive/` | Original P1 scraping, calculations, data and images |
| `legacy/instagram/` | Original P2 API script and CSV snapshots |
| `legacy/notebooks/` | Original P3 notebook, kept byte-for-byte |

## Quality checks

```bash
ruff check --select E4,E7,E9,F src tests
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

GitHub Actions executes these checks for pushes and PRs. Live scrape/API tests are intentionally excluded from CI; no production credentials are required.

## Scope and limitations

- Legacy Selenium scripts use APIs removed in Selenium 4 and likely stale site selectors; they are preserved as reference implementations, not supported entry points. Browser binaries are not distributed with the maintained tree; modern Selenium can manage drivers if later browser automation is rebuilt.
- The archived notebook is preserved, not converted to scripts. Its embedded outputs and historical data require a separate review before reuse.
- Historical images, workbooks and sample CSVs are retained for traceability. Treat Instagram sample content and any embedded identifiers as potentially sensitive before republishing or redistributing.
- No Docker image or deployment pipeline is introduced for this local, read-only tool collection. There is no verified server or scheduled job to deploy.

See [architecture](docs/architecture.md), [security and data policy](docs/security.md) and [migration notes](docs/migration.md).
