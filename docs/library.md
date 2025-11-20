# AgentM Library (Literate Notes)

This file alone defines the reusable `agentm` package and its accompanying regression tests. Nothing under `src/agentm/**` or `tests/test_sanity.py` is tracked in Git; they are regenerated from the code blocks below via `task docs:tangle`.

The reusable AgentM package is intentionally tiny for now, but we still want it generated from prose so that deleting `src/` and running `task docs:tangle` recreates the full tree. Each section below contains the authoritative code for one module.

## Package version surface

```python file=src/agentm/__init__.py
"""Top-level package for AgentM."""

__version__ = "0.0.0"
```

### Contract test

The following pytest module keeps the package honest by verifying this version export remains a string. Because the test sits beside the description, usage and enforcement stay in sync.

```python file=tests/test_sanity.py
import agentm


def test_version_is_string():
    assert isinstance(agentm.__version__, str)
```

## Algebra layer hook

```python file=src/agentm/algebra/__init__.py
"""AgentM algebra layer starter."""
```

## Backends layer hook

```python file=src/agentm/backends/__init__.py
"""AgentM backends layer starter."""
```

## Runtime layer hook

```python file=src/agentm/runtime/__init__.py
"""AgentM runtime layer starter."""
```

## Visualization layer hook

```python file=src/agentm/viz/__init__.py
"""AgentM viz layer starter."""
```
