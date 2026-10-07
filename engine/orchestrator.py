import argparse, json, random
import pandas as pd
from core.strategy_dna import make_seed
from research.researcher import Researcher
from .store import init_db, save_strategy
from .queue import enqueue

def demo_df(n=1500, seed=42):
    rng = random.Random(seed)
    price = 100.0
    rows=[]
    for i in range(n):
        drift = 0.0002 if (i//250)%2==0 else -0.00015
        ret = drift + rng.gauss(0,0.008)
        o=price; c=max(1,price*(1+ret))
        h=max(o,c)*(1+rng.random()*0.004); l=min(o,c)*(1-rng.random()*0.004)
        rows.append((i,o,h,l,c,1000+rng.random()*500))
        price=c
    return pd.DataFrame(rows,columns=["timestamp","open","high","low","close","volume"])

def seed_population():
    return [make_seed("Seed-Long","long"), make_seed("Seed-Short","short"),
            make_seed("Seed-Wide-Long","long",30,70)]

def run(db="strategy_lab.db", count=25):
    con=init_db(db)
    population=seed_population()
    hashes=set()
    for d in population:
        if save_strategy(con,d):
            hashes.add(d.hash()); enqueue(con,d)
    researcher=Researcher(random.Random(42))
    candidates=researcher.propose(population,hashes,count)
    for d in candidates:
        if save_strategy(con,d):
            enqueue(con,d)
    print(f"Queued {len(candidates)+len(population)} experiments.")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--db",default="strategy_lab.db")
    p.add_argument("--experiments",type=int,default=25)
    p.add_argument("--demo",action="store_true")
    a=p.parse_args()
    run(a.db,a.experiments)
