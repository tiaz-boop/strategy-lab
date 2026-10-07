import random, copy
from core.strategy_dna import StrategyDNA

def mutate(dna, rng=None):
    rng = rng or random.Random()
    d = copy.deepcopy(dna.to_dict())
    d.pop("id", None)
    d["generation"] = dna.generation + 1
    d["parent_a"] = dna.id
    d["parent_b"] = None
    e = d["entry"]
    if e["type"] == "trend_rsi":
        e["rsi_low"] = max(15, min(45, e["rsi_low"] + rng.choice([-5,-3,3,5])))
        e["rsi_high"] = min(85, max(55, e["rsi_high"] + rng.choice([-5,-3,3,5])))
        e["fast_ema"] = max(5, min(50, e["fast_ema"] + rng.choice([-5,-2,2,5])))
    d["exit"]["stop_atr"] = round(max(0.5, min(5.0, d["exit"]["stop_atr"] + rng.choice([-0.25,0.25]))), 2)
    d["exit"]["target_atr"] = round(max(0.75, min(8.0, d["exit"]["target_atr"] + rng.choice([-0.5,0.5]))), 2)
    d["name"] = dna.name + "-M"
    d.pop("id", None)
    return StrategyDNA(**d)

def simplify(dna):
    d = dna.to_dict()
    d["filters"] = []
    d["name"] = dna.name + "-S"
    d["generation"] = dna.generation + 1
    d["parent_a"] = dna.id
    d["parent_b"] = None
    d.pop("id", None)
    return StrategyDNA(**d)
