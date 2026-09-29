"""Tests for lifecycle state machine and handover."""

from __future__ import annotations

from pathlib import Path

import pytest

from epe.orchestration.lifecycle import Lifecycle, State, create_lifecycle, transition
from epe.orchestration.project import create_project
from epe.orchestration.handover import execute_handover


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
