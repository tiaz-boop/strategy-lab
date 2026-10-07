import pytest
from live.executor import place_order, LiveTradingDisabled

def test_live_is_disabled():
    with pytest.raises(LiveTradingDisabled):
        place_order("BTCUSDT","buy",1)
