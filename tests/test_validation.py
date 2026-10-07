from engine.orchestrator import demo_df
from core.strategy_dna import make_seed
from validation.validator import validate

def test_validation_schema():
    r=validate(demo_df(400),make_seed("v"))
    assert 0 <= r["score"] <= 100
    assert "holdout" in r
    assert "overfit_risk" in r
