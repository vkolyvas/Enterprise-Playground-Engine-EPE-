"""Consistency validator: cross-artifact contradictions and classification conflicts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

from epe.core.frontmatter import read_doc
from epe.validation.engine import Finding, make_finding


def validate_consistency(artifact_path: Path, context: dict[str, Any]) -> Iterable[Finding]:
    project_paths = context.get("project_paths")
    if project_paths is None:
        return
    project_root = project_paths.project_root
    doc = read_doc(artifact_path)
    body = doc.body

    # Product catalog: capability classification must not contradict usage in scope.md
    if doc.metadata.get("contract") == "product.catalog":
        unsupported_in_use = []
        for line in body.splitlines():
            m = re.match(r"\|\s*(CAP-\d+)\s*\|\s*([^|]+?)\s*\|\s*unsupported", line)
            if m:
                cap, _name = m.group(1), m.group(2)
                # Check scope.md
                scope = project_root / "presales" / "scope.md"
                if scope.exists() and cap in read_doc(scope).body:
                    unsupported_in_use.append(cap)
        for cap in unsupported_in_use:
            yield make_finding(
                validator="consistency",
                severity="blocker",
                location=f"{artifact_path}#{cap}",
                message=(
                    f"Capability {cap} is classified as 'unsupported' in the catalog "
                    "but referenced in presales scope."
                ),
                kind="unsupported_capability_in_use",
                remediation="Reclassify the capability or remove it from scope.",
            )

    # Presales handover: requirements marked 'rejected' must not appear in architecture
    if doc.metadata.get("contract") == "presales.handover":
        rejected = set(re.findall(r"REQ-\d+\s*\[status:\s*rejected\]", body))
        arch = project_root / "architecture" / "hld.md"
        if arch.exists() and rejected:
            arch_body = read_doc(arch).body
            for req in rejected:
                if req.split(" ")[0] in arch_body:
                    yield make_finding(
                        validator="consistency",
                        severity="error",
                        location=f"{artifact_path}#{req}",
                        message=f"Rejected requirement {req} appears in architecture HLD.",
                    )
