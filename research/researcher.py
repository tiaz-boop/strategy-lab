"""Heuristic autonomous researcher for V0.5.

This is deliberately model-independent. It can later be backed by an LLM,
but all generated strategies still pass through the safe Strategy Grammar.
"""

import random
from core.strategy_dna import make_seed, StrategyDNA
from core.strategy_grammar import validate_strategy
from .mutation import mutate, simplify
from .crossover import crossover
from .novelty import novelty_score
from .questions import QUESTIONS

class Researcher:
    def __init__(self, rng=None):
        self.rng = rng or random.Random(42)

    def questions(self):
        return [{"question": q, "hypothesis": h} for q,h in QUESTIONS]

    def propose(self, population, known_hashes, count=25):
        if not population:
            population = [
                make_seed("Seed-Long", "long"),
                make_seed("Seed-Short", "short"),
                make_seed("Seed-Long-Wide", "long", 30, 70),
                make_seed("Seed-Short-Wide", "short", 30, 70),
            ]
        out = []
        while len(out) < count:
            op = self.rng.choice(["mutate","mutate","simplify","crossover"])
            if op == "crossover" and len(population) >= 2:
                dna = crossover(self.rng.choice(population), self.rng.choice(population))
            elif op == "simplify":
                dna = simplify(self.rng.choice(population))
            else:
                dna = mutate(self.rng.choice(population), self.rng)
            ok, _ = validate_strategy(dna)
            if ok and dna.hash() not in known_hashes:
                out.append(dna)
                known_hashes.add(dna.hash())
        return out
