# Validation philosophy

A strategy is not considered trustworthy because it has a high backtest return.

V0.5 evaluates:
- train performance
- test performance
- independent holdout performance
- walk-forward fold consistency
- trade-order Monte Carlo stress
- parameter perturbation
- drawdown
- trade count
- overfit risk

The final holdout should not be used to guide strategy generation in a production research run. V0.5 demonstrates the boundary; future versions should maintain a physically separate holdout dataset.
