"""Handover records between stages."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from epe.core.frontmatter import read_doc, write_doc
from epe.core.logging import audit_log


@dataclass
class HandoverRecord:
    project_id: str
    from_stage: str
    to_stage: str
    artifact_path: str
    contract: str
    checksum_sha256: str
    at: str
    findings: list[dict[str, Any]] = field(default_factory=list)
    approved_by: str | None = None
    rationale: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


# Stage-to-stage artifact map for handover validation
HANDOVER_ARTIFACTS: dict[tuple[str, str], str] = {
    ("product", "presales"): "product/readiness.md",
    ("presales", "architecture"): "presales/handover.md",
    ("architecture", "delivery"): "architecture/solution-baseline.md",
    ("delivery", "product"): "delivery/feedback.md",
}


def required_artifacts_for_transition(stage: str) -> list[str]:
    """Return the artifacts that must exist for this stage to be considered complete."""
    return {
        "product": ["product/definition.md", "product/catalog.md",
                    "product/guardrails.md", "product/readiness.md"],
        "presales": ["presales/discovery.md", "presales/qualification.md",
                     "presales/scope.md", "presales/sow.md", "presales/handover.md"],
        "architecture": ["architecture/validation.md", "architecture/hld.md",
                         "architecture/security.md", "architecture/lld.md",
                         "architecture/cost.md", "architecture/solution-baseline.md"],
        "delivery": ["delivery/plan.md", "delivery/test.md", "delivery/acceptance.md",
                     "delivery/onboarding.md", "delivery/operations.md",
                     "delivery/handover.md", "delivery/feedback.md"],
    }.get(stage, [])


def execute_handover(
    *,
    paths,
    from_stage: str,
    to_stage: str,
    approved_by: str,
    rationale: str | None = None,
) -> HandoverRecord:
    """Validate the upstream artifact, stamp approval metadata, and write a record."""
    artifact_rel = HANDOVER_ARTIFACTS.get((from_stage, to_stage))
    if not artifact_rel:
        raise ValueError(f"No handover artifact configured for {from_stage} -> {to_stage}")
    artifact_path = paths.project_root / artifact_rel
    if not artifact_path.exists():
        raise FileNotFoundError(
            f"Handover artifact missing for {from_stage} -> {to_stage}: {artifact_path}"
        )
    doc = read_doc(artifact_path)
    contract = doc.metadata.get("contract", f"{from_stage}.handover")

    # Stamp approval
    doc.metadata["status"] = "approved"
    doc.metadata["approved_by"] = approved_by
    doc.metadata["approved_at"] = datetime.now(timezone.utc).isoformat()
    write_doc(artifact_path, doc.body, doc.metadata)

    record = HandoverRecord(
        project_id=paths.project_id,
        from_stage=from_stage,
        to_stage=to_stage,
        artifact_path=str(artifact_path),
        contract=contract,
        checksum_sha256=doc.metadata.get("checksum_sha256", ""),
        at=datetime.now(timezone.utc).isoformat(),
        approved_by=approved_by,
        rationale=rationale,
    )

    handovers_dir = paths.project_root / "handovers"
    handovers_dir.mkdir(parents=True, exist_ok=True)
    record_path = handovers_dir / f"{from_stage}-to-{to_stage}-{record.at.replace(':', '')}.json"
    record_path.write_text(
        json.dumps(record.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    audit_log(
        paths.project_audit_log,
        {
            "ts": record.at,
            "actor": approved_by,
            "action": "handover",
            "from_stage": from_stage,
            "to_stage": to_stage,
            "artifact": str(artifact_path),
            "contract": contract,
        },
    )
    return record
