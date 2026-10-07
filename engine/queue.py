import json, uuid, socket
from .store import connect

def enqueue(con, dna):
    jid = uuid.uuid4().hex
    con.execute("""INSERT INTO experiments
    (id,strategy_id,status,symbol,interval) VALUES (?,?,?,?,?)""",
    (jid,dna.id,"queued","BTCUSDT",dna.timeframe))
    con.commit()
    return jid

def claim(con, worker=None):
    worker = worker or socket.gethostname()
    con.execute("BEGIN IMMEDIATE")
    row = con.execute("SELECT * FROM experiments WHERE status='queued' ORDER BY created_at LIMIT 1").fetchone()
    if not row:
        con.commit()
        return None
    con.execute("UPDATE experiments SET status='running',worker=?,started_at=CURRENT_TIMESTAMP WHERE id=?",
                (worker,row["id"]))
    con.commit()
    return row

def finish(con, jid, status="done", error=None):
    con.execute("UPDATE experiments SET status=?,error=?,finished_at=CURRENT_TIMESTAMP WHERE id=?",
                (status,error,jid))
    con.commit()
