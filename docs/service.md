# AgentM Service Sketch (Literate Notes)

This document is the canonical description of how the AgentM service is used and tested. The code cited here tangles into `tests/test_service_e2e.py` and `src/agentm_service/**` via `task docs:tangle`; no other files in Git contain service behavior.

The AgentM library will stay focused on reusable primitives under `src/agentm/`, while the service is a thin orchestration layer that exposes those primitives over a long-lived process (think CLI/HTTP workers). To keep code and prose coupled, this document captures the intent while the tests pin the behavior.

## First executable story

We start with an end-to-end test that treats the service strictly as an executable module. No internal APIs are assumed—only that `python -m agentm_service` exists and can be queried for status. The test and usage documentation live right here so the narrative, verification, and generated file stay aligned.

```python file=tests/test_service_e2e.py
"""Usage-oriented regression test for `python -m agentm_service --status`."""

import subprocess
import sys


def test_service_cli_reports_status():
    result = subprocess.run(
        [sys.executable, "-m", "agentm_service", "--status"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "AgentM service" in result.stdout
```

Running `task test -k service` passes once `task docs:tangle` has generated the service package from `docs/service_impl.md`. If the generated files are missing (for example, after deleting `src/agentm_service/` and the test above), rerun the tangling task and the regenerated sources keep this story honest.

## Second executable story – listing AgentM modules

Now that the service proves it can report status, we want to dogfood the library layout by exposing the modules that ship with the `agentm` package. The desired usage is:

```
python -m agentm_service --list-modules
```

and the output should enumerate the modules discovered inside `agentm` (algebra, backends, runtime, viz, etc.). The CLI will introspect the installed `agentm` package (i.e., the build artifact generated from `docs/library.md`). The regression test below embeds that expectation and tangles into `tests/test_service_list_modules.py`:

```python file=tests/test_service_list_modules.py
import subprocess
import sys


def test_service_lists_modules():
    result = subprocess.run(
        [sys.executable, "-m", "agentm_service", "--list-modules"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "agentm.algebra" in result.stdout
```

This will fail until `docs/service_impl.md` grows support for the flag. Once implemented, both service tests should pass together.

## Separation of concerns

- **Library (`agentm`)**: continues to host algebra/backends/runtime/viz building blocks that remain importable without any service dependencies.
- **Service (`agentm_service`)**: will live beside the library (e.g., `src/agentm_service/`) and depend on `agentm`. This keeps deployable concerns—configuration, adapters, CLI entrypoints—isolated.
- **Tasks**: orchestration stays in `Taskfile.yml`; new service helpers (run, watch, package) can be added without touching the core library workflow.

This literate loop—doc → test (`tests/test_service_e2e.py`) → code (`docs/service_impl.md` → `src/agentm_service/__main__.py`)—is how we will keep the inevitable service glue honest while protecting backward compatibility for pure library consumers.
