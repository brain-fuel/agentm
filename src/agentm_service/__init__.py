"""AgentM service package.

This stays thin so the reusable `agentm` library remains decoupled from how we
expose it as a long-lived process.
"""

from .__main__ import main

__all__ = ["main"]
