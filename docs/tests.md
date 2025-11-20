# AgentM Tests (Literate Notes)

All test modules are generated from this document so that deleting `tests/` and running `task docs:tangle` restores the full suite.

## Library sanity check

This asserts the package keeps exporting a string version. It guards the simplest contract for downstream consumers.

```python file=tests/test_sanity.py
import agentm


def test_version_is_string():
    assert isinstance(agentm.__version__, str)
```

## Service end-to-end contract

Links back to `docs/service.md` and `docs/service_impl.md`. The test drives the expected CLI behavior and remains backward-compatible because it only shells out through the public module entrypoint.

```python file=tests/test_service_e2e.py
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
