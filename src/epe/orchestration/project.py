"""Project setup and per-project context."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

from epe.core.paths import EpePaths
from epe.core.logging import audit_log


@dataclass
class Project:
    project_id: str
    paths: EpePaths

    def initial_state(self) -> dict:
        return {
            "project_id": self.project_id,
            "stage": "product",
            "status": "active",
            "gates": {
                "product": {"status": "pending"},
                "presales": {"qualification": "pending", "scope": "pending", "handover": "pending"},
                "architecture": {
                    "requirements": "pending",
                    "hld": "pending",
                    "lld": "pending",
                },
                "delivery": {"deployment": "pending", "acceptance": "pending"},
            },
            "history": [],
        }


def create_project(paths: EpePaths, project_id: str, *, customer: str | None = None) -> Project:
    """Create the project directory tree and write an initial state file."""
    paths.ensure_project_layout()
    project = Project(project_id=project_id, paths=paths)
    state_path = paths.project_state
    if not state_path.exists():
        state = project.initial_state()
        if customer:
            state["customer"] = customer
        state_path.write_text(
            yaml.safe_dump(state, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    # Optional context directory
    context_dir = paths.project_root / "context"
    (context_dir / "opportunity.md").write_text(
        f"# Opportunity\n\nProject ID: {project_id}\nCustomer: {customer or '(unset)'}\n",
        encoding="utf-8",
    )
    audit_log(
        paths.project_audit_log,
        {
            "ts": datetime.now(timezone.utc).isoformat(),
            "actor": "cli",
            "action": "create_project",
            "target": project_id,
            "customer": customer,
        },
    )
    return project
