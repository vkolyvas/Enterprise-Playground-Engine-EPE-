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

    return app


# WSGI/ASGI entry point
app = create_app()
