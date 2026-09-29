"""Security validator: secrets and sensitivity rules."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from epe.core.frontmatter import read_doc
from epe.ingestion.security import scan_for_secrets
from epe.validation.engine import Finding, make_finding


def validate_security(artifact_path: Path, context: dict[str, Any]) -> Iterable[Finding]:
    doc = read_doc(artifact_path)
    findings = scan_for_secrets(doc.body, location=str(artifact_path))
    for sf in findings:
        yield make_finding(
            validator="security",
            severity="blocker",
            location=f"{artifact_path}#({sf.kind})",
            message=f"Potential secret detected ({sf.kind}): {sf.excerpt}",
            remediation="Remove the secret. If the artifact legitimately references a key, "
                         "use a placeholder and store the value in a vault.",
        )

    # Sensitivity mismatches
    sensitivity = doc.metadata.get("sensitivity")
    if sensitivity == "public":
        body = doc.body
        if "internal" in body.lower() or "confidential" in body.lower():
            yield make_finding(
                validator="security",
                severity="warning",
                location=str(artifact_path),
                message="Public-sensitivity artifact mentions internal/confidential terms.",
            )
