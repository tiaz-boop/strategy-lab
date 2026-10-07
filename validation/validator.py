from core.backtester import backtest
from core.metrics import metrics
from .robustness import walk_forward, monte_carlo, perturbation

def validate(df, dna):
    n = len(df)
    train = df.iloc[:int(n*0.60)]
    test = df.iloc[int(n*0.60):int(n*0.85)]
    holdout = df.iloc[int(n*0.85):]

    train_m = metrics(backtest(train, dna))
    test_r = backtest(test, dna)
    test_m = metrics(test_r)
    hold_m = metrics(backtest(holdout, dna))

    wf = walk_forward(df.iloc[:int(n*0.85)], dna)
    positive_folds = sum(x["return"] > 0 for x in wf) / max(len(wf),1)
    mc = monte_carlo(test_r["trades"])
    pert = perturbation(train, dna)
    pert_positive = sum(x["return"] > 0 for x in pert) / max(len(pert),1)

    robustness = (
        0.30 * min(test_m["profit_factor"]/2, 1) +
        0.25 * positive_folds +
        0.20 * min(max(test_m["return"],0)/0.10, 1) +
        0.15 * pert_positive +
        0.10 * max(0, 1-test_m["max_drawdown"])
    )
    overfit_risk = max(0, min(1,
        0.45 * max(0, train_m["return"]-test_m["return"]) +
        0.35 * max(0, test_m["return"]-hold_m["return"]) +
        0.20 * (1-positive_folds)
    ))
    score = max(0, min(100, robustness*100 - overfit_risk*25))
    lifecycle = "rejected"
    if score >= 70 and test_m["trades"] >= 5 and hold_m["return"] >= -0.05:
        lifecycle = "promising"
    if score >= 82 and hold_m["return"] > 0:
        lifecycle = "elite"

    return {
        "score": score,
        "lifecycle": lifecycle,
        "train": train_m,
        "test": test_m,
        "holdout": hold_m,
        "walk_forward": wf,
        "monte_carlo": mc,
        "perturbation": pert,
        "robustness": robustness,
        "overfit_risk": overfit_risk
    }
