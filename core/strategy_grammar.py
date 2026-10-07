"""Safe strategy grammar. Generated strategies are data, not executable code."""

INDICATORS = {"ema", "rsi", "atr", "volume_sma"}
ENTRY_TYPES = {"trend_rsi", "breakout_volume", "mean_reversion"}
SIDES = {"long", "short"}

def validate_strategy(dna):
    if dna.side not in SIDES:
        return False, "invalid side"
    e = dna.entry
    if e.get("type") not in ENTRY_TYPES:
        return False, "invalid entry type"
    if e.get("type") == "trend_rsi":
        for k in ("fast_ema","slow_ema","rsi_period","rsi_low","rsi_high"):
            if k not in e:
                return False, f"missing {k}"
        if e["fast_ema"] >= e["slow_ema"]:
            return False, "fast EMA must be below slow EMA"
    if e.get("type") == "breakout_volume":
        if e.get("lookback", 20) < 2:
            return False, "lookback too small"
    if dna.exit.get("stop_atr", 0) <= 0 or dna.exit.get("target_atr", 0) <= 0:
        return False, "ATR exits must be positive"
    return True, "ok"
