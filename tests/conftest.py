"""Shared test fixtures."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pytest

from epe.core.config import EpeConfig, load_config
from epe.core.paths import EpePaths


@pytest.fixture
def tmp_repo(tmp_path: Path, monkeypatch) -> Path:
    """Create a temporary copy of the EPE repo config tree."""
    repo = tmp_path / "epe"
    (repo / "config").mkdir(parents=True)
    (repo / "knowledge").mkdir()
    (repo / "sources").mkdir()
    (repo / "schemas").mkdir()
    (repo / "templates").mkdir()
    (repo / "workflows").mkdir()
    (repo / "projects").mkdir()
    (repo / "data").mkdir()

    # Copy config files
    here = Path(__file__).resolve().parents[1]
    for cfg in ("system.yaml", "models.yaml", "stages.yaml", "tools.yaml",
                "ingestion.yaml", "embeddings.yaml", "retrieval.yaml",
                "validation.yaml", "output.yaml"):
        src = here / "config" / cfg
        if src.exists():
            shutil.copy(src, repo / "config" / cfg)

    monkeypatch.setattr("epe.core.paths.REPO_ROOT", repo)
    return repo


@pytest.fixture
def config(tmp_repo: Path) -> EpeConfig:
    return load_config(repo_root=tmp_repo)


@pytest.fixture
def paths(config: EpeConfig, tmp_repo: Path) -> EpePaths:
    return EpePaths(config, project_id="TEST-001")
