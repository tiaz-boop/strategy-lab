from core.strategy_dna import make_seed
from core.strategy_grammar import validate_strategy

def test_seed_is_valid():
    d=make_seed("test")
    ok,msg=validate_strategy(d)
    assert ok, msg
    assert len(d.hash()) == 20
