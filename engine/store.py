import sqlite3, json, uuid
from pathlib import Path

def connect(db="strategy_lab.db"):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    return con

def init_db(db="strategy_lab.db"):
    schema = Path(__file__).resolve().parents[1] / "database" / "schema.sql"
    con = connect(db)
    con.executescript(schema.read_text())
    con.commit()
    return con

def save_strategy(con, dna, novelty=0):
    try:
        con.execute("""INSERT INTO strategies
        (id,canonical_hash,strategy_json,generation,lifecycle,novelty,parent_a,parent_b)
        VALUES (?,?,?,?,?,?,?,?)""",
        (dna.id,dna.hash(),json.dumps(dna.to_dict()),dna.generation,"queued",
         novelty,dna.parent_a,dna.parent_b))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def save_validation(con, dna, report):
    con.execute("""INSERT INTO validations
    (id,strategy_id,score,train_return,test_return,profit_factor,win_rate,
     max_drawdown,robustness,overfit_risk,report_json)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (uuid.uuid4().hex,dna.id,report["score"],report["train"]["return"],
     report["test"]["return"],report["test"]["profit_factor"],report["test"]["win_rate"],
     report["test"]["max_drawdown"],report["robustness"],report["overfit_risk"],
     json.dumps(report)))
    con.execute("UPDATE strategies SET lifecycle=? WHERE id=?", (report["lifecycle"],dna.id))
    con.commit()

def log_event(con, strategy_id, event_type, payload):
    con.execute("INSERT INTO events(strategy_id,event_type,payload_json) VALUES (?,?,?)",
                (strategy_id,event_type,json.dumps(payload)))
    con.commit()
