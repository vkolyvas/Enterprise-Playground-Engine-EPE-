"""Filesystem paths for EPE.

All paths are computed from the repo root, which is the parent of `src/`.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from epe.core.config import EpeConfig


REPO_ROOT = Path(__file__).resolve().parents[3]


class EpePaths:
    """Resolved filesystem paths."""

    def __init__(self, config: "EpeConfig", project_id: str | None = None) -> None:
        self.config = config
        self.repo_root = REPO_ROOT
        self.config_root = self.repo_root / "config"
        self.knowledge_root = self.repo_root / config.system.paths.knowledge_root
        self.sources_root = self.repo_root / config.system.paths.sources_root
        self.schemas_root = self.repo_root / config.system.paths.schemas_root
        self.templates_root = self.repo_root / config.system.paths.templates_root
        self.workflows_root = self.repo_root / config.system.paths.workflows_root
        self.audit_root = self.repo_root / config.system.paths.audit_root
        self.projects_root = self.repo_root / config.system.paths.projects_root
        self.project_id = project_id

    @property
    def project_root(self) -> Path:
        if not self.project_id:
            raise ValueError("project_id is not set on this EpePaths instance")
        return self.projects_root / self.project_id

    # Knowledge namespaces ---------------------------------------------------

    @property
    def knowledge_global(self) -> Path:
        return self.knowledge_root / "global"

    def knowledge_namespace(self, namespace: str) -> Path:
        return self.knowledge_root / namespace

    # Sources ----------------------------------------------------------------

    @property
    def sources_incoming(self) -> Path:
        return self.sources_root / "incoming"

    @property
    def sources_classified(self) -> Path:
        return self.sources_root / "classified"

    @property
    def sources_processed(self) -> Path:
        return self.sources_root / "processed"

    @property
    def sources_rejected(self) -> Path:
        return self.sources_root / "rejected"

    # Project subdirs --------------------------------------------------------

    @property
    def project_product(self) -> Path:
        return self.project_root / "product"

    @property
    def project_presales(self) -> Path:
        return self.project_root / "presales"

    @property
    def project_architecture(self) -> Path:
        return self.project_root / "architecture"

    @property
    def project_delivery(self) -> Path:
        return self.project_root / "delivery"

    @property
    def project_requirements(self) -> Path:
        return self.project_root / "requirements"

    @property
    def project_decisions(self) -> Path:
        return self.project_root / "decisions"

    @property
    def project_risks(self) -> Path:
        return self.project_root / "risks"

    @property
    def project_questions(self) -> Path:
        return self.project_root / "questions"

    @property
    def project_state(self) -> Path:
        return self.project_root / "state.yaml"

    @property
    def project_audit_log(self) -> Path:
        return self.project_root / ".audit.log"

    @property
    def project_validation_dir(self) -> Path:
        return self.project_root / ".validation"

    @property
    def project_dashboard(self) -> Path:
        return self.project_root / "dashboard.md"

    # Constructors -----------------------------------------------------------

    def project_source_incoming(self) -> Path:
        """Per-project incoming folder; created on demand."""
        if not self.project_id:
            raise ValueError("project_id is not set on this EpePaths instance")
        path = self.project_root / "sources" / "incoming"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def ensure_project_layout(self) -> None:
        """Create the standard project directory tree."""
        if not self.project_id:
            raise ValueError("project_id is not set on this EpePaths instance")
        for sub in (
            "context",
            "sources",
            "product",
            "presales",
            "architecture",
            "delivery",
            "decisions",
            "risks",
            "questions",
            "requirements",
            ".validation",
        ):
            (self.project_root / sub).mkdir(parents=True, exist_ok=True)
