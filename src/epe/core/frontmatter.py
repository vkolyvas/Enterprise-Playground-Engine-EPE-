"""Markdown + YAML frontmatter helpers."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import frontmatter


@dataclass
class ParsedDoc:
    """A parsed Markdown document with YAML frontmatter."""

    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def contract(self) -> str | None:
        return self.metadata.get("contract")

    @property
    def stage(self) -> str | None:
        return self.metadata.get("stage")

    @property
    def status(self) -> str | None:
        return self.metadata.get("status")

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def section_text(self, heading: str) -> str | None:
        """Extract body text under a Markdown heading (## or # level)."""
        body = self.body
        lines = body.splitlines()
        target = heading.strip().lower()
        collecting = False
        out: list[str] = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#"):
                if collecting:
                    break
                heading_text = stripped.lstrip("#").strip().lower()
                if heading_text == target:
                    collecting = True
                continue
            if collecting:
                out.append(line)
        text = "\n".join(out).strip()
        return text or None

    def has_section(self, heading: str) -> bool:
        return self.section_text(heading) is not None


def read_doc(path: Path) -> ParsedDoc:
    if not path.exists():
        raise FileNotFoundError(f"No such file: {path}")
    text = path.read_text(encoding="utf-8")
    fm = frontmatter.loads(text)
    return ParsedDoc(path=path, metadata=dict(fm.metadata or {}), body=fm.content)


def write_doc(
    path: Path,
    body: str,
    metadata: dict[str, Any],
    *,
    sort_keys: bool = True,
) -> Path:
    """Write a Markdown document with YAML frontmatter and a SHA256 checksum."""
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = dict(metadata)
    meta.setdefault("checksum_sha256", "")
    fm = frontmatter.Post(body, **meta)
    payload = frontmatter.dumps(fm)
    checksum = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    meta["checksum_sha256"] = checksum
    fm = frontmatter.Post(body, **meta)
    final = frontmatter.dumps(fm)
    path.write_text(final, encoding="utf-8")
    return path


def verify_checksum(path: Path) -> bool:
    """Verify the document's SHA256 checksum matches its body."""
    doc = read_doc(path)
    expected = doc.metadata.get("checksum_sha256")
    if not expected:
        return False
    raw = path.read_text(encoding="utf-8")
    # The checksum is computed over (body + frontmatter) excluding the
    # checksum field itself. We re-parse and recompute.
    fm = frontmatter.Post(doc.body, **{k: v for k, v in doc.metadata.items() if k != "checksum_sha256"})
    payload = frontmatter.dumps(fm)
    actual = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return actual == expected
