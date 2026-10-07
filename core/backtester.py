import pandas as pd
from .signals import build_indicators, entry_signal

def backtest(df, dna, fee_rate=0.001, slippage_rate=0.0005, initial_balance=10000):
    x = build_indicators(df, dna)
    sig = entry_signal(df, dna).fillna(False)
    balance = float(initial_balance)
    trades = []
    position = None
    max_bars = int(dna.exit.get("max_bars", 48))
    stop_atr = float(dna.exit["stop_atr"])
    target_atr = float(dna.exit["target_atr"])

    for i in range(1, len(x)):
        row = x.iloc[i]
        if position is None and bool(sig.iloc[i-1]) and pd.notna(row.atr):
            entry = float(row.open) * (1 + slippage_rate if dna.side == "long" else 1 - slippage_rate)
            position = {"i": i, "entry": entry, "atr": float(row.atr)}
            continue
        if position is None:
            continue

        side = 1 if dna.side == "long" else -1
        stop = position["entry"] - side * stop_atr * position["atr"]
        target = position["entry"] + side * target_atr * position["atr"]
        held = i - position["i"]
        exit_price = None

        if dna.side == "long":
            if row.low <= stop: exit_price = stop
            elif row.high >= target: exit_price = target
        else:
            if row.high >= stop: exit_price = stop
            elif row.low <= target: exit_price = target

        if exit_price is None and held >= max_bars:
            exit_price = float(row.close)

        if exit_price is not None:
            exit_price *= (1 - slippage_rate if dna.side == "long" else 1 + slippage_rate)
            gross = side * (exit_price - position["entry"]) / position["entry"]
            pnl = balance * (gross - 2 * fee_rate)
            balance += pnl
            trades.append({"entry_i": position["i"], "exit_i": i,
                           "entry": position["entry"], "exit": exit_price,
                           "pnl": pnl, "return_pct": pnl / max(balance-pnl, 1e-9)})
            position = None

    return {"ending_balance": balance, "return": balance/initial_balance-1,
            "trades": trades}
