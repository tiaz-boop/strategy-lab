import random, numpy as np
from core.backtester import backtest
from core.metrics import metrics

def walk_forward(df, dna, folds=4):
    n = len(df)
    results = []
    for k in range(folds):
        start = int(k*n/folds)
        end = int((k+1)*n/folds)
        chunk = df.iloc[start:end]
        if len(chunk) < 80:
            continue
        m = metrics(backtest(chunk, dna))
        results.append(m)
    return results

def monte_carlo(trades, runs=250, seed=42):
    if not trades:
        return {"median": 0, "p05": 0, "p95": 0}
    rng = random.Random(seed)
    vals = []
    pnls = [float(t["pnl"]) for t in trades]
    for _ in range(runs):
        sample = [rng.choice(pnls) for _ in pnls]
        vals.append(sum(sample))
    vals.sort()
    return {"median": float(np.median(vals)),
            "p05": float(np.percentile(vals,5)),
            "p95": float(np.percentile(vals,95))}

def perturbation(df, dna, variants=8):
    from research.mutation import mutate
    rng = random.Random(7)
    vals = []
    for _ in range(variants):
        m = mutate(dna, rng)
        vals.append(metrics(backtest(df, m)))
    return vals
