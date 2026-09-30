"""Tests for lifecycle state machine and handover."""

from __future__ import annotations

from pathlib import Path

import pytest

from epe.orchestration.lifecycle import Lifecycle, State, create_lifecycle, transition
from epe.orchestration.project import create_project
from epe.orchestration.handover import execute_handover
from epe.tracking.registry import DocumentRegistry
from epe.validation.completeness import (
    validate_stage_completeness,
    validate_gate_completeness,
    validate_all,
)


def test_lifecycle_initial_state(tmp_path: Path, paths) -> None:
    state_path = paths.project_state
    state_path.parent.mkdir(parents=True, exist_ok=True)
    lc = create_lifecycle(state_path)
    assert lc.state.current == State.PRODUCT_ACTIVE


def test_lifecycle_transitions(tmp_path: Path, paths) -> None:
    state_path = paths.project_state
    state_path.parent.mkdir(parents=True, exist_ok=True)
    lc = create_lifecycle(state_path)
    lc.transition(State.PRODUCT_READY)
    assert lc.state.current == State.PRODUCT_READY
    lc.transition(State.PRESALES_ACTIVE)
    assert lc.state.current == State.PRESALES_ACTIVE


def test_lifecycle_illegal_transition(tmp_path: Path, paths) -> None:
    state_path = paths.project_state
    state_path.parent.mkdir(parents=True, exist_ok=True)
    lc = create_lifecycle(state_path)
    with pytest.raises(Exception):
        lc.transition(State.SERVICE_LIVE)


def test_handover_requires_artifact(tmp_path: Path, paths) -> None:
    paths.ensure_project_layout()
    with pytest.raises(FileNotFoundError):
        execute_handover(
            paths=paths,
            from_stage="presales",
            to_stage="architecture",
            approved_by="tester",
        )


def test_handover_stamps_approval(tmp_path: Path, paths) -> None:
    paths.ensure_project_layout()
    # create a minimal handover artifact
    target = paths.project_presales / "handover.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "---\ncontract: presales.handover\nversion: 1\nstage: presales\n"
        "status: draft\nopportunity: OPP-1\ncustomer: Acme\ngenerated_at: x\ngenerated_by: test\n---\n\nbody\n",
        encoding="utf-8",
    )
    record = execute_handover(
        paths=paths,
        from_stage="presales",
        to_stage="architecture",
        approved_by="lead_architect",
    )
    assert record.approved_by == "lead_architect"
    assert record.from_stage == "presales"
    assert record.to_stage == "architecture"
    # verify the artifact was stamped
    text = target.read_text(encoding="utf-8")
    assert "approved_by: lead_architect" in text
    assert "status: approved" in text


def _write_doc(path: Path, content: str = "body content") -> None:
    """Write a minimal document with required frontmatter."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\ncontract: {path.stem}\nversion: 1\nstage: {path.parent.name}\n"
        f"status: approved\nopportunity: TEST-001\ncustomer: Test\n"
        f"generated_at: 2026-01-01T00:00:00Z\ngenerated_by: test\n---\n\n{content}\n",
        encoding="utf-8",
    )


def test_gate_blocked_state_when_mandatory_docs_missing(tmp_path: Path, paths) -> None:
    """Verify BLOCKED state when mandatory documents are missing."""
    # Create only some of the mandatory documents for presales
    paths.ensure_project_layout()
    _write_doc(paths.project_presales / "discovery.md")
    _write_doc(paths.project_presales / "qualification.md")
    # scope.md, sow.md, handover.md are missing

    registry = DocumentRegistry.from_project(paths.project_root, "TEST-001")
    result = validate_gate_completeness(paths.project_root, registry)

    assert result["presales"]["readiness"] == "BLOCKED"
    assert "scope.md" in result["presales"]["missing_documents"]
    assert "sow.md" in result["presales"]["missing_documents"]
    assert "handover.md" in result["presales"]["missing_documents"]


def test_gate_ready_state_when_all_mandatory_docs_approved(tmp_path: Path, paths) -> None:
    """Verify READY state when all mandatory documents are present and approved."""
    paths.ensure_project_layout()

    # Write all mandatory presales documents as approved
    for doc in ["discovery.md", "qualification.md", "scope.md", "sow.md", "handover.md"]:
        _write_doc(paths.project_presales / doc)

    registry = DocumentRegistry.from_project(paths.project_root, "TEST-001")
    result = validate_gate_completeness(paths.project_root, registry)

    assert result["presales"]["readiness"] == "READY"
    assert result["presales"]["completeness_score"] == 1.0
    assert result["presales"]["all_approved"] is True
    assert len(result["presales"]["missing_documents"]) == 0


def test_gate_warning_state_when_docs_present_not_approved(tmp_path: Path, paths) -> None:
    """Verify WARNING state when docs present but not all approved."""
    paths.ensure_project_layout()

    # Write all mandatory documents with draft status
    for doc in ["discovery.md", "qualification.md", "scope.md", "sow.md", "handover.md"]:
        p = paths.project_presales / doc
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            f"---\ncontract: {p.stem}\nversion: 1\nstage: presales\n"
            f"status: draft\nopportunity: TEST-001\ncustomer: Test\n"
            f"generated_at: 2026-01-01T00:00:00Z\ngenerated_by: test\n---\n\nbody\n",
            encoding="utf-8",
        )

    registry = DocumentRegistry.from_project(paths.project_root, "TEST-001")
    result = validate_gate_completeness(paths.project_root, registry)

    assert result["presales"]["readiness"] == "WARNING"
    assert result["presales"]["completeness_score"] == 1.0
    assert result["presales"]["all_approved"] is False


def test_gate_architecture_blocked_without_solution_baseline(tmp_path: Path, paths) -> None:
    """Verify architecture stage is BLOCKED without solution-baseline.md."""
    paths.ensure_project_layout()

    # Write some architecture docs but NOT solution-baseline.md
    for doc in ["validation.md", "hld.md", "security.md", "lld.md", "cost.md"]:
        _write_doc(paths.project_architecture / doc)

    registry = DocumentRegistry.from_project(paths.project_root, "TEST-001")
    result = validate_gate_completeness(paths.project_root, registry)

    assert result["architecture"]["readiness"] == "BLOCKED"
    assert "solution-baseline.md" in result["architecture"]["missing_documents"]


def test_gate_delivery_blocked_without_solution_baseline(tmp_path: Path, paths) -> None:
    """Verify delivery stage is BLOCKED without architecture solution-baseline."""
    paths.ensure_project_layout()

    # Write all architecture docs including solution-baseline.md (approved)
    for doc in ["validation.md", "hld.md", "security.md", "lld.md", "cost.md", "solution-baseline.md"]:
        _write_doc(paths.project_architecture / doc)

    registry = DocumentRegistry.from_project(paths.project_root, "TEST-001")
    result = validate_gate_completeness(paths.project_root, registry)

    # Architecture should now be READY
    assert result["architecture"]["readiness"] == "READY"
    # Delivery should still be BLOCKED because its own mandatory docs are missing
    assert result["delivery"]["readiness"] == "BLOCKED"


def test_validate_all_returns_overall_status(tmp_path: Path, paths) -> None:
    """Verify validate_all returns overall_status and gate_status."""
    paths.ensure_project_layout()

    # Write all mandatory documents for all stages as approved
    for doc in ["definition.md", "catalog.md", "guardrails.md", "readiness.md"]:
        _write_doc(paths.project_product / doc)
    for doc in ["discovery.md", "qualification.md", "scope.md", "sow.md", "handover.md"]:
        _write_doc(paths.project_presales / doc)
    for doc in ["validation.md", "hld.md", "security.md", "lld.md", "cost.md", "solution-baseline.md"]:
        _write_doc(paths.project_architecture / doc)
    for doc in ["plan.md", "test.md", "acceptance.md", "onboarding.md", "operations.md", "handover.md", "feedback.md"]:
        _write_doc(paths.project_delivery / doc)

    registry = DocumentRegistry.from_project(paths.project_root, "TEST-001")
    result = validate_all(paths.project_root, registry)

    assert result["overall_status"] == "READY"
    assert result["overall_blockers"] == 0
    for stage in ["product", "presales", "architecture", "delivery"]:
        assert result["gate_status"][stage]["readiness"] == "READY"

