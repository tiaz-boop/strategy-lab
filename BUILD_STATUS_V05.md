# V0.5 Build Status

Implemented:
- Strategy DNA
- Safe strategy grammar
- Indicators and signal engine
- Backtester with fees/slippage
- Metrics
- Mutation
- Crossover
- Simplification
- Novelty detection
- Research questions
- Autonomous heuristic researcher
- Walk-forward validation
- Monte Carlo stress
- Perturbation testing
- Overfit risk
- Strategy lifecycle
- Genealogy fields
- SQLite database
- Queue and workers
- MEXC public candle collector
- Paper account
- Dashboard
- Tests
- GitHub Actions CI
- Explicit live-trading safety boundary

Known V0.5 limitations:
- Research data defaults to deterministic demo data in workers.
- SQLite is not a billion-scale distributed backend.
- Researcher is model-independent heuristic logic, not an external LLM.
- Dashboard is intentionally lightweight and unauthenticated for localhost development.
- Live execution is disabled.
