CREATE TABLE IF NOT EXISTS strategies (
    id TEXT PRIMARY KEY,
    canonical_hash TEXT UNIQUE NOT NULL,
    strategy_json TEXT NOT NULL,
    generation INTEGER DEFAULT 0,
    lifecycle TEXT DEFAULT 'queued',
    novelty REAL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    parent_a TEXT,
    parent_b TEXT
);

CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    status TEXT DEFAULT 'queued',
    symbol TEXT,
    interval TEXT,
    worker TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    started_at TEXT,
    finished_at TEXT,
    error TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
);

CREATE TABLE IF NOT EXISTS validations (
    id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    score REAL,
    train_return REAL,
    test_return REAL,
    profit_factor REAL,
    win_rate REAL,
    max_drawdown REAL,
    robustness REAL,
    overfit_risk REAL,
    report_json TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
);

CREATE TABLE IF NOT EXISTS research_questions (
    id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    hypothesis TEXT,
    status TEXT DEFAULT 'open',
    priority REAL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    answered_at TEXT
);

CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id TEXT NOT NULL,
    symbol TEXT,
    side TEXT,
    entry_time TEXT,
    exit_time TEXT,
    entry REAL,
    exit REAL,
    pnl REAL,
    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id TEXT,
    event_type TEXT NOT NULL,
    payload_json TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
