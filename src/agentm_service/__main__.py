"""Command-line entry point for the AgentM service.

The CLI intentionally depends on the public `agentm` package so that we dogfood
its surface area instead of reaching into implementation detail.
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
