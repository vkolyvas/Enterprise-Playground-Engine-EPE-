"""Plain text / CSV / JSON / YAML extractor."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

from epe.ingestion.extractors import ExtractedDocument


def extract(path: Path) -> ExtractedDocument:
    ext = path.suffix.lower()
    text = path.read_text(encoding="utf-8", errors="replace")
    tables: list[list[list[str]]] = []
    structure: dict = {"format": "text"}

    if ext == ".csv":
        with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.reader(f)
            table = [row for row in reader]
            if table:
                tables.append(table)
        structure["format"] = "csv"
    elif ext in {".json"}:
        try:
            structure["format"] = "json"
            structure["parsed"] = json.loads(text)
        except json.JSONDecodeError as e:
            structure["parse_error"] = str(e)
    elif ext in {".yaml", ".yml"}:
        try:
            structure["format"] = "yaml"
            structure["parsed"] = yaml.safe_load(text)
        except yaml.YAMLError as e:
            structure["parse_error"] = str(e)

    return ExtractedDocument(
        path=path,
        text=text,
        structure=structure,
        pages=[],
        sections=[],
        tables=tables,
        extractor="text",
    )
