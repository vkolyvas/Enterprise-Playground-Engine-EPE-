"""Tests for the validation engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from epe.core.frontmatter import write_doc
from epe.validation.engine import run_validators


def test_structural_missing_required_fields(tmp_path: Path, paths) -> None:
    p = tmp_path / "bad.md"
    p.write_text("# Hi\n\nContent here with REQ-001 referenced inline.\n", encoding="utf-8")
    report = run_validators(p, project_paths=paths)
    # Should have findings about missing frontmatter fields.
    msgs = [f.message for f in report.findings]
    assert any("contract" in m or "version" in m or "stage" in m for m in msgs)


def test_content_missing_section(tmp_path: Path, paths) -> None:
    p = tmp_path / "missing.md"
    write_doc(
        p,
        body="## Problem statement\n\nSome text.\n",
        metadata={
            "contract": "product.definition",
            "version": 1,
            "stage": "product",
            "status": "draft",
            "generated_at": "2026-09-29T10:00:00Z",
            "generated_by": "test",
        },
    )
    report = run_validators(p, project_paths=paths)
    msgs = [f.message for f in report.findings]
    assert any("Product name" in m for m in msgs)


def test_security_detects_secrets(tmp_path: Path, paths) -> None:
    p = tmp_path / "leak.md"
    write_doc(
        p,
        body="AWS key: AKIAIOSFODNN7EXAMPLE\n## Body\n",
        metadata={
            "contract": "product.definition",
            "version": 1,
            "stage": "product",
            "status": "draft",
            "generated_at": "2026-09-29T10:00:00Z",
            "generated_by": "test",
        },
    )
    report = run_validators(p, project_paths=paths)
    assert any(f.validator == "security" for f in report.findings)


def test_passing_artifact(tmp_path: Path, paths) -> None:
    p = tmp_path / "ok.md"
    write_doc(
        p,
        body=(
            "# OK\n\n"
            "## Product name and one-line description\nReference DOC-001.\n\n"
            "## Problem statement\nReference DOC-001.\n\n"
            "## Target users and personas\nReference DOC-001.\n\n"
            "## Use cases (must / should / could)\nReference DOC-001.\n\n"
            "## Out-of-scope (explicit non-goals)\nReference DOC-001.\n\n"
            "## Differentiators\nReference DOC-001.\n\n"
            "## Evidence references (with document IDs)\nReference DOC-001.\n"
        ),
        metadata={
            "contract": "product.definition",
            "version": 1,
            "stage": "product",
            "status": "draft",
            "generated_at": "2026-09-29T10:00:00Z",
            "generated_by": "test",
        },
    )
    report = run_validators(p, project_paths=paths)
    blocker = [f for f in report.findings if f.severity == "blocker"]
    assert not blocker, [f.message for f in blocker]
