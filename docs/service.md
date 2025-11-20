# AgentM Service Sketch (Literate Notes)

The AgentM library will stay focused on reusable primitives under `src/agentm/`, while the service is a thin orchestration layer that exposes those primitives over a long-lived process (think CLI/HTTP workers). To keep code and prose coupled, this document captures the intent while the tests pin the behavior.

## First executable story

We start with an end-to-end test that treats the service strictly as an executable module. No internal APIs are assumed—only that `python -m agentm_service` exists and can be queried for status. The canonical test case lives in the literate tests document (`docs/tests.md`, tangled into `tests/test_service_e2e.py`).

Running `task test -k service` is expected to fail for now because the service package does not exist. That failure is the next TODO, and once resolved the same command becomes our regression harness. The code that satisfies this story lives in `docs/service_impl.md`, which in turn tangles into `src/agentm_service/__main__.py` via `task docs:tangle`. Delete `src/agentm_service/` and `tests/test_service_e2e.py`, run that task, and the generated sources are recreated from the docs.

## Separation of concerns

- **Library (`agentm`)**: continues to host algebra/backends/runtime/viz building blocks that remain importable without any service dependencies.
- **Service (`agentm_service`)**: will live beside the library (e.g., `src/agentm_service/`) and depend on `agentm`. This keeps deployable concerns—configuration, adapters, CLI entrypoints—isolated.
- **Tasks**: orchestration stays in `Taskfile.yml`; new service helpers (run, watch, package) can be added without touching the core library workflow.

This literate loop—doc → test (`tests/test_service_e2e.py`) → code (`docs/service_impl.md` → `src/agentm_service/__main__.py`)—is how we will keep the inevitable service glue honest while protecting backward compatibility for pure library consumers.
