import argparse
from engine.worker import run_worker
p=argparse.ArgumentParser(); p.add_argument("--db",default="strategy_lab.db")
p.add_argument("--once",action="store_true"); a=p.parse_args()
run_worker(a.db,a.once)