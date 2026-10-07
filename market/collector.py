import sqlite3, time, requests
from pathlib import Path

URL="https://api.mexc.com/api/v3/klines"

def collect(symbol="BTCUSDT", interval="5m", limit=1000, db="strategy_lab.db"):
    r=requests.get(URL,params={"symbol":symbol,"interval":interval,"limit":limit},timeout=20)
    r.raise_for_status()
    rows=r.json()
    con=sqlite3.connect(db)
    con.execute("""CREATE TABLE IF NOT EXISTS candles(
        symbol TEXT, interval TEXT, open_time INTEGER,
        open REAL, high REAL, low REAL, close REAL, volume REAL,
        PRIMARY KEY(symbol,interval,open_time))""")
    for x in rows:
        con.execute("INSERT OR REPLACE INTO candles VALUES(?,?,?,?,?,?,?,?)",
                    (symbol,interval,int(x[0]),float(x[1]),float(x[2]),float(x[3]),
                     float(x[4]),float(x[5])))
    con.commit(); con.close()
    return len(rows)
