"""Tests for the dashboard projections."""

from __future__ import annotations

from pathlib import Path

import pytest

from epe.dashboard.projections import (
    project_dashboard_markdown,
    project_list,
    project_summary,
)
from epe.orchestration.project import create_project


def test_project_list_empty(tmp_repo: Path, paths) -> None:
    assert project_list(paths.projects_root) == []


def test_project_summary(tmp_repo: Path, paths) -> None:
    create_project(paths, "TEST-001", customer="Acme")
    summary = project_summary(paths.projects_root / "TEST-001")
    assert summary["project_id"] == "TEST-001"
    assert summary["stage"] == "product"


def test_project_dashboard_markdown(tmp_repo: Path, paths) -> None:
    create_project(paths, "TEST-001", customer="Acme")
    md = project_dashboard_markdown(paths.projects_root / "TEST-001")
    assert "# EPE — Project TEST-001" in md
    assert "Handover readiness" in md
