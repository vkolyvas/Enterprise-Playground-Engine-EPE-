"""Chunking strategies for the knowledge layer."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from epe.ingestion.extractors import ExtractedDocument


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source_document_id: str
    source_path: str
    namespace: str
    position: int
    section_heading: str = ""
    section_level: int = 0
    metadata: dict | None = None

    def to_index(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "source_document_id": self.source_document_id,
            "source_path": self.source_path,
            "namespace": self.namespace,
            "position": self.position,
            "section_heading": self.section_heading,
            "section_level": self.section_level,
            "text": self.text,
            "metadata": self.metadata or {},
        }


def chunk_by_section(
    document: ExtractedDocument,
    *,
    namespace: str,
    source_document_id: str,
    max_chars: int = 4000,
    overlap_chars: int = 400,
) -> list[Chunk]:
    """Chunk an extracted document by its existing section structure."""
    out: list[Chunk] = []
    if document.sections:
        for i, section in enumerate(document.sections):
            text = "\n".join(section.get("lines", [])).strip()
            if not text:
                continue
            heading = section.get("heading", "")
            level = section.get("level", 0)
            # further split large sections
            for j, part in enumerate(_split_with_overlap(text, max_chars, overlap_chars)):
                out.append(
                    Chunk(
                        chunk_id=_chunk_id(namespace, source_document_id, i, j, part),
                        text=part,
                        source_document_id=source_document_id,
                        source_path=str(document.path),
                        namespace=namespace,
                        position=len(out),
                        section_heading=heading,
                        section_level=level,
                    )
                )
    else:
        for j, part in enumerate(_split_with_overlap(document.text, max_chars, overlap_chars)):
            out.append(
                Chunk(
                    chunk_id=_chunk_id(namespace, source_document_id, 0, j, part),
                    text=part,
                    source_document_id=source_document_id,
                    source_path=str(document.path),
                    namespace=namespace,
                    position=len(out),
                )
            )
    return out


def _chunk_id(namespace: str, doc_id: str, section_idx: int, part_idx: int, text: str) -> str:
    h = hashlib.sha256(f"{namespace}|{doc_id}|{section_idx}|{part_idx}|{text}".encode("utf-8")).hexdigest()[:12].upper()
    return f"KNW-{namespace}-{h}"


def _split_with_overlap(text: str, max_chars: int, overlap_chars: int) -> Iterable[str]:
    if len(text) <= max_chars:
        yield text
        return
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        yield text[start:end]
        if end == len(text):
            return
        start = max(end - overlap_chars, start + 1)


def chunks_to_index_file(chunks: list[Chunk], path: Path) -> Path:
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump([c.to_index() for c in chunks], f, ensure_ascii=False, indent=2)
    return path
