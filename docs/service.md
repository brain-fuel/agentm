# AgentM Service Sketch (Literate Notes)

The AgentM library will stay focused on reusable primitives under `src/agentm/`, while the service is a thin orchestration layer that exposes those primitives over a long-lived process (think CLI/HTTP workers). To keep code and prose coupled, this document captures the intent while the tests pin the behavior.

## First executable story

We start with an end-to-end test that treats the service strictly as an executable module. No internal APIs are assumed—only that `python -m agentm_service` exists and can be queried for status. The test currently lives in `tests/test_service_e2e.py`:

```python
import subprocess
import sys


def test_service_cli_reports_status():
    """End-to-end expectation for the AgentM service executable."""
    result = subprocess.run(
        [sys.executable, "-m", "agentm_service", "--status"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "AgentM service" in result.stdout
```

Running `task test -k service` is expected to fail for now because the service package does not exist. That failure is the next TODO, and once resolved the same command becomes our regression harness.

## Separation of concerns

- **Library (`agentm`)**: continues to host algebra/backends/runtime/viz building blocks that remain importable without any service dependencies.
- **Service (`agentm_service`)**: will live beside the library (e.g., `src/agentm_service/`) and depend on `agentm`. This keeps deployable concerns—configuration, adapters, CLI entrypoints—isolated.
- **Tasks**: orchestration stays in `Taskfile.yml`; new service helpers (run, watch, package) can be added without touching the core library workflow.

This literate loop—doc → test → code—is how we will keep the inevitable service glue honest while protecting backward compatibility for pure library consumers.
