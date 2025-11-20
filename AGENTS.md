# Notes for Future Agents (Professor-style Briefing)

Son, before you touch a single line, internalize this: **there is no “loose” source code in this repository.** Every Python file under `src/` and every test under `tests/` is merely an artifact regenerated from Markdown. Our workflow is intentionally pedantic because it keeps prose, tests, and implementation perfectly entangled.

## What exists (and where)

- `README.md`: spells out the high-level install dance. Memorize the order:
  1. `task docs:tangle` — rebuild `src/` and `tests/` from the literate sources.
  2. `python -m venv .venv && source .venv/bin/activate`
  3. `pip install -e ".[dev]" && pytest`
- `Taskfile.yml`: automation nerve center. Every meaningful task (lint, typecheck, test) depends on the tangling step, so no excuses about stale code.
- `docs/library.md`: **sole source of truth** for the reusable `agentm` package and its regression test (`tests/test_sanity.py`). Delete `src/agentm/**` or the test—they come back the moment you tangle this doc.
- `docs/service.md`: usage narrative plus the end-to-end test (`tests/test_service_e2e.py`). Think of it as the “what the CLI should do” manifesto.
- `docs/service_impl.md`: describes the actual service implementation (`src/agentm_service/__init__.py` + `__main__.py`). If you edit those generated files directly, you are wrong.
- `docs/tools.md`: authoritative source for every script under `tools/` (including the tangler itself). Delete `tools/tangle_docs.py`, run `task docs:tangle`, and it reappears with its warning header.
- `tools/tangle_docs.py`: tiny Python script that reads code fences like ```python file=src/...``` from the docs and writes the real files with warning headers.
- `.gitignore`: aggressively ignores `src/` and `tests/` so Git only tracks the Markdown + tooling.

## How to work safely

1. Run `task docs:tangle`. Verify it prints `[tangle] wrote ...` for every target. (If it fails, fix the Markdown, not the generated files.)
2. Make your prose + code changes inside the relevant doc (`docs/library.md`, `docs/service.md`, `docs/service_impl.md`).
3. Re-run `task docs:tangle` so the artifacts refresh.
4. Run `task qa` (or at least `task test`) to prove the doc-driven code behaves.
5. Commit the Markdown + tooling; never stage files inside `src/` or `tests/`.

## What we already know

- Python 3.11 virtualenv exists locally (`.venv/`). Treat that as standard.
- Version-controlled history shows prior commits formalizing the literate loop (`build: treat docs as source of truth`, `test: generate suite from docs`, etc.). Respect that intent when you extend the system.
- Networking may be restricted (pushes can fail if DNS is blocked), so plan accordingly.

Follow these rules and the next agent—or even your absent-minded professor—can reconstruct the entire project from text alone. Deviate, and you will spend Saturday re-deriving theorems about missing files.
