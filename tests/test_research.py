from research.researcher import Researcher
from core.strategy_dna import make_seed

def test_researcher_proposes_unique():
    p=[make_seed("a"),make_seed("b","short")]
    out=Researcher().propose(p,set(x.hash() for x in p),10)
    assert len(out)==10
    assert len({x.hash() for x in out})==10
