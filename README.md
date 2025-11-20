# AgentM Starter Repo

Starter project layout for AgentM under the Eclipse Public License v2.0.

Use TDD and expand incrementally.

## Install

```
task docs:tangle
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Literate source workflow

Absolutely no Python source files live in Git—they are all generated from Markdown. Specifically:

- Library modules + their regression tests: `docs/library.md`
- Service implementation: `docs/service_impl.md`
- Service usage + end-to-end test: `docs/service.md`

Delete `src/` and `tests/` at any time; the following command regenerates the entire tree from those documents:

```
task docs:tangle
```

to regenerate the full source + test tree from documentation before running tests or modifying any code. The standard `task test`/`task qa` commands already depend on this tangling step, so every workflow rebuilds code from its literate source of truth.
