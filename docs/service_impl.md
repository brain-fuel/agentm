# AgentM Service Implementation (Literate Notes)

This file is the implementation-side counterpart to `docs/service.md`. While `docs/service.md` motivates the executable story and embeds the end-to-end test, this document shows the code that satisfies that story and references the same test for traceability. **Every byte of service implementation must originate here**; the generated `src/agentm_service/**` files exist only as build artifacts.

All code snippets below are tangled into the actual source tree via `task docs:tangle`. Delete the generated files, re-run that task, and the sources are recreated from this Markdown, making this document the source of truth.

## Cross reference

- Story + test: `docs/service.md` → `tests/test_service_e2e.py`
- Implementation: this file → `src/agentm_service/__main__.py`

Keeping the code in a single Markdown file also makes it clear what still needs explaining: whenever we change the Python module, we should update the prose around it.

## CLI bootstrap

The service code is intentionally tiny: it consumes the public `agentm` package, surfaces `--status`, and refuses to do anything implicit. Here is the complete module:

```python file=src/agentm_service/__init__.py
"""AgentM service package.

Auto-generated from docs/service_impl.md by tools/tangle_docs.py.
"""

from .__main__ import main

__all__ = ["main"]
```

```python file=src/agentm_service/__main__.py
"""Command-line entry point for the AgentM service.

The literate source of truth for this module lives in docs/service_impl.md. Keep
that document and this file in sync whenever behavior changes.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

import agentm


@dataclass
class CliConfig:
    """Simple data holder for CLI arguments."""

    status: bool


def parse_args(argv: list[str] | None = None) -> CliConfig:
    parser = argparse.ArgumentParser(
        prog="agentm_service",
        description="Minimal AgentM service harness for dogfooding.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Report the service readiness and exit.",
    )

    parsed = parser.parse_args(argv)
    return CliConfig(status=parsed.status)


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for `python -m agentm_service`."""
    args = parse_args(argv)

    if args.status:
        print(f"AgentM service ready (agentm {agentm.__version__})")
        return 0

    # Placeholder for future subcommands (server loop, etc.).
    print("No action specified; try --status", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

Any future behavior (looping runtimes, HTTP adapters, etc.) should be added here along with an explanation and a new test reference so the literate loop stays intact.
