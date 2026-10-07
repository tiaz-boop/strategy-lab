from .indicators import ema, rsi, atr, volume_sma

def build_indicators(df, dna):
    e = dna.entry
    out = df.copy()
    out["atr"] = atr(out, 14)
    typ = e["type"]
    if typ == "trend_rsi":
        out["fast_ema"] = ema(out.close, e["fast_ema"])
        out["slow_ema"] = ema(out.close, e["slow_ema"])
        out["rsi"] = rsi(out.close, e["rsi_period"])
    elif typ == "breakout_volume":
        n = e.get("lookback", 20)
        out["prior_high"] = out.high.rolling(n).max().shift(1)
        out["prior_low"] = out.low.rolling(n).min().shift(1)
        out["vol_sma"] = volume_sma(out.volume, e.get("volume_period", 20))
    elif typ == "mean_reversion":
        out["ema"] = ema(out.close, e.get("ema_period", 50))
        out["rsi"] = rsi(out.close, e.get("rsi_period", 14))
    return out

def entry_signal(df, dna):
    x = build_indicators(df, dna)
    e = dna.entry
    typ = e["type"]
    if typ == "trend_rsi":
        if dna.side == "long":
            return (x.fast_ema > x.slow_ema) & (x.rsi <= e["rsi_low"])
        return (x.fast_ema < x.slow_ema) & (x.rsi >= e["rsi_high"])
    if typ == "breakout_volume":
        if dna.side == "long":
            return (x.close > x.prior_high) & (x.volume > x.vol_sma)
        return (x.close < x.prior_low) & (x.volume > x.vol_sma)
    if dna.side == "long":
        return (x.close < x["ema"]) & (x.rsi < e.get("rsi_low", 30))
    return (x.close > x["ema"]) & (x.rsi > e.get("rsi_high", 70))
