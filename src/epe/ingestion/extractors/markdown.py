"""Markdown extractor."""

from __future__ import annotations

import re
from pathlib import Path

from epe.ingestion.extractors import ExtractedDocument

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def extract(path: Path) -> ExtractedDocument:
    text = path.read_text(encoding="utf-8", errors="replace")
    sections: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            if current is not None:
                sections.append(current)
            current = {"level": len(m.group(1)), "heading": m.group(2).strip(), "lines": []}
        else:
            if current is None:
                current = {"level": 0, "heading": "", "lines": []}
            current["lines"].append(line)
    if current is not None:
        sections.append(current)
    return ExtractedDocument(
        path=path,
        text=text,
        structure={"format": "markdown"},
        pages=[],
        sections=sections,
        tables=[],
        extractor="markdown",
    )
