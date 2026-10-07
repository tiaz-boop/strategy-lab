# Strategy Lab V0.5

Autonomous crypto strategy research laboratory.

Strategy Lab continuously generates, mutates, crosses, simplifies, validates, ranks, and records trading-strategy hypotheses. It is designed to research strategies using historical/replay data first and keeps real-money execution disabled by default.

## What V0.5 does

- Strategy DNA: machine-readable strategy definitions.
- Strategy grammar: safe building blocks instead of arbitrary generated Python.
- Research loop: question → hypothesis → experiment → validation → learning.
- Mutation, crossover, simplification, novelty and duplicate detection.
- Strategy genealogy and parent/child lineage.
- Promotion lifecycle: `queued → testing → promising → walk_forward → paper → elite` plus `rejected/retired`.
- Walk-forward validation, Monte Carlo trade-order stress, parameter perturbation and holdout protection.
- SQLite persistence for local development.
- Queue + worker architecture for parallel experiments.
- MEXC public candle collector with no trading credentials required.
- Paper-trading simulator boundary.
- Dashboard API/UI.
- Unit tests and GitHub Actions CI.
- Live execution module is a hard-disabled safety boundary in V0.5.

## Quick start

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt

python scripts/init_db.py
python scripts/run_research.py --demo --experiments 25
python scripts/start_dashboard.py
```

Open `http://127.0.0.1:8000`.

Run tests:

```bash
pytest -q
```

Run a single worker:

```bash
python scripts/run_worker.py
```

Collect public MEXC candles:

```bash
python scripts/collect_data.py
```

## Important safety boundary

V0.5 does **not** place real-money orders. `live/executor.py` deliberately raises an error. Do not remove this boundary casually.

Research results are not proof of profitability. Strategies must survive independent holdout data, realistic costs/slippage, multiple regimes and paper trading before any future live-execution implementation is considered.

## Architecture

```text
Market Data
    ↓
Dataset / Replay
    ↓
Researcher
    ↓
Strategy DNA / Grammar
    ↓
Queue
    ↓
Workers
    ↓
Backtest + Walk Forward + Monte Carlo + Perturbation
    ↓
Robustness / Overfit / Novelty
    ↓
Genealogy + Lifecycle
    ↓
Dashboard / Paper Trading
```

## Repository map

- `core/` strategy representation and backtesting
- `research/` autonomous hypothesis/evolution logic
- `validation/` robustness tests
- `market/` public market data collection
- `engine/` orchestration and workers
- `paper/` paper-only execution simulation
- `live/` intentionally disabled live boundary
- `dashboard/` monitoring API/UI
- `database/` schema
- `tests/` automated tests
- `docs/` design documentation

## Scaling path

SQLite is intentionally used for V0.5 simplicity. It is not a billion-experiment production database. A later distributed version should move queue/results to PostgreSQL/Redis or another distributed architecture, separate compute workers, partition datasets, and preserve a never-touched final holdout set.

GitHub stores the source. The actual experiment compute should eventually run on a VPS/cloud/container fleet rather than inside the Git repository itself.
