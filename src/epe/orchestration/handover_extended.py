"""Extended handover — generates formal handoff package with artifact manifest.

Extends ``orchestration/handover.py`` with a complete manifest of all stage
artifacts, their versions, completeness status, and traceability links.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from epe.tracking.registry import DocumentRegistry
from epe.tracking.lineage import LineageComputer
from epe.orchestration.handover import (
    HANDOVER_ARTIFACTS,
    execute_handover,
    HandoverRecord,
)
from epe.validation.completeness import validate_stage_completeness


@dataclass
class HandoverManifest:
    """A formal handoff package listing all artifacts with their status."""

    project_id: str
    from_stage: str
    to_stage: str
    at: str
    approved_by: str
    rationale: str | None = None

    # Manifest of all documents in the source stage
    documents: list[dict[str, Any]] = field(default_factory=list)

    # Traceability summary
    requirement_count: int = 0
    component_count: int = 0
    task_count: int = 0
    test_count: int = 0

    # Stage completeness
    completeness_score: float = 0.0
    all_approved: bool = False

    # Open items
    open_risks: list[str] = field(default_factory=list)
    open_decisions: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "from_stage": self.from_stage,
            "to_stage": self.to_stage,
            "at": self.at,
            "approved_by": self.approved_by,
            "rationale": self.rationale,
            "documents": self.documents,
            "requirement_count": self.requirement_count,
            "component_count": self.component_count,
            "task_count": self.task_count,
            "test_count": self.test_count,
            "completeness_score": self.completeness_score,
            "all_approved": self.all_approved,
            "open_risks": self.open_risks,
            "open_decisions": self.open_decisions,
            "open_questions": self.open_questions,
        }


def build_manifest(
    project_root: Path,
    from_stage: str,
    to_stage: str,
    registry: DocumentRegistry | None = None,
) -> HandoverManifest:
    """Build a formal handover manifest for the stage transition.

    This includes:
    - All documents in the source stage with status/version/owner
    - Traceability counts (requirements, components, tasks, tests)
    - Open items (risks, decisions, questions) found in the stage
    - Stage completeness score
    """
    if registry is None:
        registry = DocumentRegistry.from_project(project_root, project_root.name)

    lineage = LineageComputer(registry)
    stage_docs = registry.by_stage(from_stage)

    # Collect all typed IDs across the stage
    all_reqs: set[str] = set()
    all_comps: set[str] = set()
    all_tasks: set[str] = set()
    all_tests: set[str] = set()
    all_risks: set[str] = set()
    all_decisions: set[str] = set()
    all_questions: set[str] = set()

    doc_manifests: list[dict[str, Any]] = []
    for doc in stage_docs:
        all_reqs.update(doc.requirements)
        all_comps.update(doc.components)
        all_tasks.update(doc.tasks)
        all_tests.update(doc.tests)
        all_risks.update(doc.risks)
        all_decisions.update(doc.decisions)
        doc_manifests.append({
            "doc_id": doc.doc_id,
            "contract": doc.contract,
            "title": doc.title,
            "status": doc.status.value if hasattr(doc.status, 'value') else str(doc.status),
            "version": doc.version,
            "owner": doc.owner,
            "approved_by": doc.approved_by,
            "approved_at": doc.approved_at,
            "inputs": doc.inputs,
            "outputs": doc.outputs,
            "requirements": doc.requirements,
            "components": doc.components,
            "tasks": doc.tasks,
            "tests": doc.tests,
            "risks": doc.risks,
            "decisions": doc.decisions,
        })

    # Stage completeness
    completeness = validate_stage_completeness(project_root, from_stage, registry)

    manifest = HandoverManifest(
        project_id=project_root.name,
        from_stage=from_stage,
        to_stage=to_stage,
        at=datetime.now(timezone.utc).isoformat(),
        approved_by="",  # filled in by execute_handover
        rationale=None,
        documents=doc_manifests,
        requirement_count=len(all_reqs),
        component_count=len(all_comps),
        task_count=len(all_tasks),
        test_count=len(all_tests),
        completeness_score=completeness["completeness_score"],
        all_approved=completeness["all_approved"],
        open_risks=sorted(all_risks),
        open_decisions=sorted(all_decisions),
        open_questions=sorted(all_questions),
    )
    return manifest


def execute_handover_with_manifest(
    *,
    paths,
    from_stage: str,
    to_stage: str,
    approved_by: str,
    rationale: str | None = None,
) -> tuple[HandoverRecord, HandoverManifest]:
    """Execute the handover and generate a formal manifest.

    Returns both the HandoverRecord (written to disk) and the HandoverManifest.
    """
    project_root = paths.project_root

    # Build manifest before approval (so documents show pre-approval status)
    registry = DocumentRegistry.from_project(project_root, paths.project_id)
    manifest = build_manifest(project_root, from_stage, to_stage, registry)
    manifest.approved_by = approved_by
    manifest.rationale = rationale

    # Execute the base handover (stamps approval on the artifact)
    record = execute_handover(
        paths=paths,
        from_stage=from_stage,
        to_stage=to_stage,
        approved_by=approved_by,
        rationale=rationale,
    )

    # Write manifest alongside the handover record
    handovers_dir = project_root / "handovers"
    manifest_path = handovers_dir / f"manifest-{from_stage}-to-{to_stage}-{record.at.replace(':', '')}.json"
    manifest_path.write_text(
        __import__("json").dumps(manifest.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return record, manifest
