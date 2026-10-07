"""V0.5 safety boundary: live trading is intentionally disabled."""

class LiveTradingDisabled(RuntimeError):
    pass

def place_order(*args, **kwargs):
    raise LiveTradingDisabled(
        "Live order execution is disabled in Strategy Lab V0.5. "
        "Use research and paper trading only."
    )
