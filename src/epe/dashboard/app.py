"""FastAPI application for the EPE dashboard."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

from epe.core.config import load_config
from epe.core.paths import EpePaths
from epe.dashboard.projections import (
    project_dashboard_markdown,
    project_list,
    project_state,
    project_summary,
    lifecycle_documents_summary,
    lifecycle_stage_view,
    lifecycle_lineage_view,
    lifecycle_gates_view,
    solution_manager_cockpit,
    governance_summary,
    milestone_summary,
    task_summary,
    rfp_summary,
)


def create_app(*, config_path: Path | None = None) -> FastAPI:
    config = load_config()
    paths = EpePaths(config)

    app = FastAPI(
        title="EPE Dashboard",
        description="Read-only projections over EPE lifecycle state and artifacts.",
        version="0.1.0",
    )

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/projects")
    def list_projects() -> list[dict]:
        return project_list(paths.projects_root)

    @app.get("/projects/{project_id}")
    def get_project(project_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return project_summary(proj_root)

    @app.get("/projects/{project_id}/state")
    def get_state(project_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return project_state(proj_root / "state.yaml")

    @app.get("/projects/{project_id}/dashboard.md", response_class=PlainTextResponse)
    def get_dashboard_md(project_id: str) -> str:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return project_dashboard_markdown(proj_root)

    @app.get("/config")
    def get_config() -> dict:
        return config.model_dump(mode="json")

    # Lifecycle document views
    @app.get("/projects/{project_id}/lifecycle/documents")
    def get_lifecycle_documents(project_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return lifecycle_documents_summary(proj_root)

    @app.get("/projects/{project_id}/lifecycle/stages/{stage}")
    def get_lifecycle_stage(project_id: str, stage: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        if stage not in ("product", "presales", "architecture", "delivery"):
            raise HTTPException(400, f"Invalid stage: {stage}")
        return lifecycle_stage_view(proj_root, stage)

    @app.get("/projects/{project_id}/lifecycle/lineage/{doc_id:path}")
    def get_lifecycle_lineage(project_id: str, doc_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return lifecycle_lineage_view(proj_root, doc_id)

    @app.get("/projects/{project_id}/lifecycle/gates")
    def get_lifecycle_gates(project_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return lifecycle_gates_view(proj_root)

    # Governance views
    @app.get("/projects/{project_id}/governance/cockpit")
    def get_governance_cockpit(project_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return solution_manager_cockpit(proj_root)

    @app.get("/projects/{project_id}/governance/summary")
    def get_governance_summary(project_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return governance_summary(proj_root)

    @app.get("/projects/{project_id}/governance/milestones")
    def get_milestone_summary(project_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return milestone_summary(proj_root)

    @app.get("/projects/{project_id}/governance/tasks")
    def get_task_summary(project_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return task_summary(proj_root)

    @app.get("/projects/{project_id}/governance/rfp")
    def get_rfp_summary(project_id: str) -> dict:
        proj_root = paths.projects_root / project_id
        if not proj_root.exists():
            raise HTTPException(404, f"No such project: {project_id}")
        return rfp_summary(proj_root)

    return app


# WSGI/ASGI entry point
app = create_app()
