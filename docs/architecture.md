# Architecture

V0.5 separates research from execution.

1. Market data is collected or replayed.
2. Researcher creates strategy DNA.
3. Grammar validates the strategy.
4. Queue stores experiment jobs.
5. Workers run deterministic validation.
6. Results are persisted with lineage.
7. Lifecycle rules promote or reject candidates.
8. Dashboard exposes the state.

The researcher never emits executable trading code. It emits data structures accepted by the grammar.

Future distributed deployments should replace SQLite queue operations with PostgreSQL/Redis and move workers to containers.
