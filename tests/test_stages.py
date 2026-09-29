"""Tests for stage engines running in dry-run mode."""

from __future__ import annotations

from pathlib import Path

import pytest

from epe.knowledge.engine import KnowledgeEngine
from epe.knowledge.providers import HashEmbeddingProvider, StubLLMProvider
from epe.stages.base import StageContext, run_stage


@pytest.fixture
def stage_ctx(config, paths):
    knowledge = KnowledgeEngine(
        config,
        paths,
        embedding_provider=HashEmbeddingProvider(dimensions=64),
        project_id="TEST-001",
    )
    return StageContext(
        config=config,
        paths=paths,
        knowledge=knowledge,
        llm=StubLLMProvider(),
        project_id="TEST-001",
    )


def test_product_engine_dry_run(stage_ctx, paths) -> None:
    paths.ensure_project_layout()
    result = run_stage("product", stage_ctx, dry_run=True)
    for name in ("definition", "catalog", "guardrails", "readiness"):
        assert name in result.outputs
        assert result.outputs[name].exists()


def test_presales_engine_requires_product(stage_ctx, paths) -> None:
    paths.ensure_project_layout()
    # No product readiness yet — engine still runs but should warn in preconditions
    result = run_stage("presales", stage_ctx, dry_run=True)
    for name in ("discovery", "qualification", "scope", "sow", "handover"):
        assert name in result.outputs


def test_architecture_engine_runs(stage_ctx, paths) -> None:
    paths.ensure_project_layout()
    result = run_stage("architecture", stage_ctx, dry_run=True)
    for name in ("validation", "hld", "security", "lld", "cost", "blueprint"):
        assert name in result.outputs


def test_delivery_engine_runs(stage_ctx, paths) -> None:
    paths.ensure_project_layout()
    result = run_stage("delivery", stage_ctx, dry_run=True)
    for name in ("plan", "test", "acceptance", "onboarding", "operations",
                 "handover_d", "feedback"):
        assert name in result.outputs
