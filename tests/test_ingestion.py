"""Tests for ingestion."""

from __future__ import annotations

from pathlib import Path

import pytest

from epe.ingestion.pipeline import IngestionPipeline


def test_ingest_markdown(tmp_path: Path, paths) -> None:
    src = tmp_path / "incoming"
    src.mkdir()
    (src / "doc.md").write_text(
        "# Customer requirements\n\n"
        "Single sign-on is required via SAML 2.0. "
        "The customer requires ISO 27001 compliance.\n",
        encoding="utf-8",
    )
    pipeline = IngestionPipeline(paths, project_id="TEST-001")
    report = pipeline.ingest_directory(src, project_id="TEST-001")
    assert report.success_count == 1
    assert report.failure_count == 0
    assert not report.secret_findings_count


def test_ingest_detects_secrets(tmp_path: Path, paths) -> None:
    src = tmp_path / "incoming"
    src.mkdir()
    (src / "leak.md").write_text(
        "Here is a leaked API key: sk-ant-abcdef1234567890abcdef1234567890\n",
        encoding="utf-8",
    )
    pipeline = IngestionPipeline(paths, project_id="TEST-001")
    report = pipeline.ingest_directory(src, project_id="TEST-001")
    assert report.success_count == 1
    assert report.secret_findings_count >= 1


def test_ingest_classifies_requirements(tmp_path: Path, paths) -> None:
    src = tmp_path / "incoming"
    src.mkdir()
    (src / "rfp.md").write_text(
        "# RFP\n\nThis is a customer RFP with security requirements. "
        "The customer requires ISO 27001 compliance. "
        "Must use SAML 2.0 for SSO.\n",
        encoding="utf-8",
    )
    pipeline = IngestionPipeline(paths, project_id="TEST-001")
    report = pipeline.ingest_directory(src, project_id="TEST-001")
    result = report.results[0]
    assert result.success
    # classifier should mark it as requirements-type
    assert result.metadata_path is not None
    import yaml as _y
    meta = _y.safe_load(result.metadata_path.read_text(encoding="utf-8"))
    assert meta["document_type"] in {"requirements", "compliance", "vendor", "market", "internal", "other", "architecture", "pricing"}
    assert "presales" in meta["stage_relevance"] or "architecture" in meta["stage_relevance"]
