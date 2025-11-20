# Tooling Source (Literate Notes)

All custom tooling lives in this document. Right now there is a single script, `tools/tangle_docs.py`, but the pattern generalizes. Delete `tools/` and rerun `task docs:tangle` to recreate the scripts from these fenced blocks.

```python file=tools/tangle_docs.py
#!/usr/bin/env python3
"""Tangle Markdown code blocks into source files.

Usage:
    python tools/tangle_docs.py docs/service_impl.md [...]

Each fenced code block must look like:

~~~python file=src/path/to/file.py
# code
~~~

The script writes the code (with a generated header) to the target file, making
parent directories as needed.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Dict, List

HEADER = (
    "# This file is auto-generated from {doc_path} via tools/tangle_docs.py.\n"
    "# Do not edit by hand; edit the literate source instead.\n\n"
)

FENCE = chr(96) * 3  # backtick literal without embedding three backticks here

class TangleError(Exception):
    pass


def parse_blocks(path: pathlib.Path) -> Dict[pathlib.Path, str]:
    blocks: Dict[pathlib.Path, List[str]] = {}
    inside = False
    capturing = False
    target: pathlib.Path | None = None

    for lineno, line in enumerate(path.read_text().splitlines(), start=1):
        if line.startswith(FENCE):
            if not inside:
                inside = True
                info_line = line[3:].strip()
                target = _parse_target(info_line, path, lineno)
                capturing = target is not None
                if capturing and target is not None:
                    blocks.setdefault(target, [])
                continue

            # closing fence
            inside = False
            capturing = False
            target = None
            continue

        if inside and capturing and target is not None:
            blocks[target].append(line)

    final: Dict[pathlib.Path, str] = {}
    for target_path, lines in blocks.items():
        content = "\n".join(lines).rstrip() + "\n"
        final[target_path] = content
    return final


def _parse_target(info_line: str, doc: pathlib.Path, lineno: int) -> pathlib.Path | None:
    if not info_line:
        return None
    parts = info_line.split()
    for token in parts[1:]:
        if token.startswith("file="):
            rel = token.split("=", 1)[1]
            return pathlib.Path(rel)
    return None


def tangle(doc_paths: List[pathlib.Path]) -> None:
    outputs: Dict[pathlib.Path, str] = {}
    for doc in doc_paths:
        blocks = parse_blocks(doc)
        if not blocks:
            continue
        for target, content in blocks.items():
            output = HEADER.format(doc_path=doc)
            output += content
            prev = outputs.get(target)
            if prev and prev != output:
                raise TangleError(f"Conflicting content for {target} from {doc}")
            outputs[target] = output

    if not outputs:
        raise TangleError("No literate code blocks found.")

    for target, content in outputs.items():
        target_path = target
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content)
        print(f"[tangle] wrote {target_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tangle literate docs into code.")
    parser.add_argument("docs", nargs="+", type=pathlib.Path)
    args = parser.parse_args(argv)

    try:
        tangle(args.docs)
    except TangleError as exc:
        print(f"tangle error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
