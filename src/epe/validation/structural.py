"""Structural validator: frontmatter parses, required fields present."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from epe.core.frontmatter import read_doc
from epe.validation.engine import Finding, make_finding

_REQUIRED_FIELDS = ["contract", "version", "stage", "status"]


def validate_structural(artifact_path: Path, context: dict[str, Any]) -> Iterable[Finding]:
    try:
        doc = read_doc(artifact_path)
    except Exception as e:
        yield make_finding(
            validator="structural",
            severity="blocker",
            location=str(artifact_path),
            message=f"Cannot parse artifact: {e}",
        )
        return

    for field_name in _REQUIRED_FIELDS:
        if field_name not in doc.metadata:
            yield make_finding(
                validator="structural",
                severity="error",
                location=f"{artifact_path}#frontmatter",
                message=f"Missing required frontmatter field: {field_name}",
                remediation=f"Add `{field_name}: <value>` to the YAML frontmatter.",
            )

    if "checksum_sha256" in doc.metadata and doc.metadata["checksum_sha256"]:
        from epe.core.frontmatter import verify_checksum
        if not verify_checksum(artifact_path):
            yield make_finding(
                validator="structural",
                severity="warning",
                location=str(artifact_path),
                message="Checksum does not match body — the artifact may have been modified outside the engine.",
            )

    if not doc.body or not doc.body.strip():
        yield make_finding(
            validator="structural",
            severity="blocker",
            location=str(artifact_path),
            message="Document body is empty.",
            remediation="Re-run the stage engine or provide content manually.",
        )
