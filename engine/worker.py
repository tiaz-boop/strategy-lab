import argparse, json, time, socket
import pandas as pd
from core.strategy_dna import StrategyDNA
from validation.validator import validate
from .store import init_db, connect, log_event, save_validation
from .queue import claim, finish

def load_demo(n=1500):
    from .orchestrator import demo_df
    return demo_df(n)

def run_worker(db="strategy_lab.db", once=False):
    con=init_db(db)
    while True:
        job=claim(con,socket.gethostname())
        if not job:
            if once: return
            time.sleep(2); continue
        try:
            row=con.execute("SELECT strategy_json FROM strategies WHERE id=?",(job["strategy_id"],)).fetchone()
            dna=StrategyDNA.from_dict(json.loads(row["strategy_json"]))
            df=load_demo()
            report=validate(df,dna)
            save_validation(con,dna,report)
            log_event(con,dna.id,"validation_complete",{"score":report["score"],"lifecycle":report["lifecycle"]})
            finish(con,job["id"],"done")
        except Exception as e:
            finish(con,job["id"],"failed",str(e))
            log_event(con,job["strategy_id"],"worker_error",{"error":str(e)})

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--db",default="strategy_lab.db")
    p.add_argument("--once",action="store_true")
    a=p.parse_args()
    run_worker(a.db,a.once)
