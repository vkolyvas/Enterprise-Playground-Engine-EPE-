"""Content validator: required Markdown sections present and non-empty."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from epe.core.frontmatter import read_doc
from epe.validation.engine import REQUIRED_SECTIONS, Finding, make_finding


def validate_content(artifact_path: Path, context: dict[str, Any]) -> Iterable[Finding]:
    doc = read_doc(artifact_path)
    contract = doc.metadata.get("contract")
    if not contract:
        return

    required = REQUIRED_SECTIONS.get(contract, [])
    for heading in required:
        text = doc.section_text(heading)
        if not text or not text.strip():
            yield make_finding(
                validator="content",
                severity="error",
                location=f"{artifact_path}#{heading}",
                message=f"Required section '{heading}' is missing or empty.",
                remediation=f"Add a '## {heading}' section with substantive content.",
            )

    # Catalog-specific: at least one capability row
    if contract == "product.catalog":
        if "| standard" not in doc.body and "| configurable" not in doc.body \
                and "| custom" not in doc.body and "| unsupported" not in doc.body:
            yield make_finding(
                validator="content",
                severity="warning",
                location=str(artifact_path),
                message="Catalog has no capability rows with classification.",
            )

    # Ungrounded claims: paragraphs with no DOC-/CAP-/REQ-/DEC-/TASK-/TEST-/Q- reference
    yield from _check_ungrounded(doc, artifact_path)


def _check_ungrounded(doc, artifact_path: Path) -> Iterable[Finding]:
    import re

    refs = re.compile(r"\b(DOC-\w+|CAP-\w+|REQ-\w+|DEC-\w+|TASK-\w+|TEST-\w+|Q-\w+)\b")
    paragraphs = [p for p in doc.body.split("\n\n") if p.strip()]
    for i, para in enumerate(paragraphs):
        # Skip headings and table-of-content-style lines
        if para.strip().startswith("#"):
            continue
        # Skip code fences and very short paragraphs
        if para.strip().startswith("```") or len(para.strip()) < 40:
            continue
        if not refs.search(para):
            yield make_finding(
                validator="content",
                severity="warning",
                location=f"{artifact_path}#p{i}",
                message="Paragraph has no inline reference to DOC-/CAP-/REQ-/DEC-/TASK-/TEST-/Q- IDs.",
                kind="ungrounded",
                remediation="Cite at least one source identifier in the same paragraph.",
            )
