import pandas as pd

def normalize_ohlcv(df):
    cols={"time":"timestamp","openTime":"timestamp","o":"open","h":"high","l":"low","c":"close","v":"volume"}
    x=df.rename(columns=cols).copy()
    for c in ["open","high","low","close","volume"]:
        if c in x: x[c]=pd.to_numeric(x[c],errors="coerce")
    return x.dropna(subset=["open","high","low","close"])
