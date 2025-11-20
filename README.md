# AgentM Starter Repo

Starter project layout for AgentM under the Eclipse Public License v2.0.

Use TDD and expand incrementally.

## Install

```
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Literate source workflow

All code under `src/` and tests under `tests/` are generated from the literate docs (`docs/library.md`, `docs/service_impl.md`, `docs/tests.md`). Run:

```
task docs:tangle
```

to regenerate the full source + test tree from documentation before running tests or modifying any code. The standard `task test`/`task qa` commands already depend on this tangling step.
