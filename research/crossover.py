import copy
from core.strategy_dna import StrategyDNA

def crossover(a, b):
    d = copy.deepcopy(a.to_dict())
    d["entry"] = copy.deepcopy(a.entry if a.entry["type"] == b.entry["type"] else a.entry)
    d["exit"] = copy.deepcopy(b.exit)
    d["risk"] = copy.deepcopy(a.risk)
    d["filters"] = copy.deepcopy(b.filters)
    d["name"] = f"{a.name}x{b.name}"
    d["generation"] = max(a.generation, b.generation) + 1
    d["parent_a"] = a.id
    d["parent_b"] = b.id
    d.pop("id", None)
    return StrategyDNA(**d)
