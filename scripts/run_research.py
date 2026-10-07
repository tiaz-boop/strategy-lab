import argparse
from engine.orchestrator import run
p=argparse.ArgumentParser(); p.add_argument("--db",default="strategy_lab.db")
p.add_argument("--experiments",type=int,default=25); p.add_argument("--demo",action="store_true")
a=p.parse_args(); run(a.db,a.experiments)