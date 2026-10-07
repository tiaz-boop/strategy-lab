import numpy as np

def metrics(result):
    t = result["trades"]
    if not t:
        return {"trades": 0, "win_rate": 0, "profit_factor": 0,
                "max_drawdown": 0, "return": result["return"]}
    pnls = np.array([x["pnl"] for x in t], dtype=float)
    wins, losses = pnls[pnls > 0], pnls[pnls < 0]
    eq = 10000 + np.cumsum(pnls)
    peak = np.maximum.accumulate(eq)
    dd = np.max((peak-eq)/peak) if len(eq) else 0
    pf = wins.sum()/abs(losses.sum()) if len(losses) else 99.0
    return {"trades": len(t), "win_rate": float((pnls > 0).mean()),
            "profit_factor": float(pf), "max_drawdown": float(dd),
            "return": float(result["return"])}
