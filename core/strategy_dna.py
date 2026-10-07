"""Strategy DNA: JSON-serializable, hashable strategy definitions."""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
import hashlib, json, uuid

@dataclass
class StrategyDNA:
    name: str
    side: str = "long"
    timeframe: str = "5m"
    entry: dict = field(default_factory=dict)
    exit: dict = field(default_factory=dict)
    risk: dict = field(default_factory=dict)
    filters: list = field(default_factory=list)
    generation: int = 0
    parent_a: str | None = None
    parent_b: str | None = None
    id: str = field(default_factory=lambda: "STR-" + uuid.uuid4().hex[:10].upper())

    def to_dict(self):
        return asdict(self)

    def canonical(self):
        d = self.to_dict().copy()
        d.pop("id", None)
        d.pop("generation", None)
        d.pop("parent_a", None)
        d.pop("parent_b", None)
        return json.dumps(d, sort_keys=True, separators=(",", ":"))

    def hash(self):
        return hashlib.sha256(self.canonical().encode()).hexdigest()[:20]

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

def make_seed(name, side="long", rsi_low=35, rsi_high=65):
    return StrategyDNA(
        name=name,
        side=side,
        timeframe="5m",
        entry={
            "type": "trend_rsi",
            "fast_ema": 20,
            "slow_ema": 50,
            "rsi_period": 14,
            "rsi_low": rsi_low,
            "rsi_high": rsi_high
        },
        exit={"stop_atr": 2.0, "target_atr": 3.0, "max_bars": 48},
        risk={"risk_per_trade": 0.01},
        filters=[{"type": "min_atr_pct", "value": 0.001}]
    )
