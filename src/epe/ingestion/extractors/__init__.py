"""Document extractors. Each module exposes `extract(path) -> ExtractedDocument`."""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ExtractedDocument:
    path: Path
    text: str
    structure: dict[str, Any] = field(default_factory=dict)
    pages: list[str] = field(default_factory=list)
    sections: list[dict[str, Any]] = field(default_factory=list)
    tables: list[list[list[str]]] = field(default_factory=list)
    extractor: str = "unknown"
    warnings: list[str] = field(default_factory=list)


def extract(path: Path) -> ExtractedDocument:
    """Dispatch to the right extractor based on file extension."""
    ext = path.suffix.lower().lstrip(".")
    if ext == "pdf":
        mod = importlib.import_module("epe.ingestion.extractors.pdf")
    elif ext == "docx":
        mod = importlib.import_module("epe.ingestion.extractors.docx")
    elif ext == "xlsx":
        mod = importlib.import_module("epe.ingestion.extractors.xlsx")
    elif ext == "pptx":
        mod = importlib.import_module("epe.ingestion.extractors.pptx")
    elif ext in {"md", "markdown"}:
        mod = importlib.import_module("epe.ingestion.extractors.markdown")
    elif ext in {"txt", "log", "csv", "json", "yaml", "yml"}:
        mod = importlib.import_module("epe.ingestion.extractors.text")
    else:
        raise ValueError(f"Unsupported file extension: {ext!r}")
    return mod.extract(path)
