"""Tests for config loading."""

from __future__ import annotations

from pathlib import Path

import pytest

from epe.core.config import load_config
from epe.core.errors import ConfigurationError


def test_config_loads(tmp_repo: Path) -> None:
    cfg = load_config(repo_root=tmp_repo)
    assert cfg.system.environment in {"dev", "staging", "prod"}
    assert "anthropic" == cfg.models.llm.provider
    assert set(cfg.stages.stages.keys()) == {"product", "presales", "architecture", "delivery"}
    for stage_name, stage in cfg.stages.stages.items():
        assert stage.gates, f"stage {stage_name} has no gates"


def test_gate_predicate_resolves(tmp_repo: Path) -> None:
    cfg = load_config(repo_root=tmp_repo)
    gp = cfg.gate_predicate("gate.product.readiness_approved")
    assert gp.module == "epe.validation.product.readiness_complete"
    assert gp.severity == "blocker"


def test_unknown_gate_raises(tmp_repo: Path) -> None:
    cfg = load_config(repo_root=tmp_repo)
    with pytest.raises(ConfigurationError):
        cfg.gate_predicate("gate.nope")
